"""Deploy the portable Linear skill and merge MCP defaults without replacing local choices."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


def read_config(path: Path) -> dict[str, object]:
    """Read an object without leaking malformed config values into diagnostics."""
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid JSON config at {path.name}") from error
    if not isinstance(value, dict):
        raise TypeError(f"{path.name}: expected a JSON object")
    return value


def deployment_changes(
    source: Path, destination: Path, *, overlay: Path | None = None
) -> list[tuple[Path, bytes]]:
    """Validate every input before returning the files that actually need writing."""
    default_path = source / "_bmad/custom/linear-mcp.json"
    if overlay is not None and (overlay / "_bmad/custom/linear-mcp.json").exists():
        default_path = overlay / "_bmad/custom/linear-mcp.json"
    defaults = read_config(default_path)
    default_servers = defaults.get("mcpServers")
    if not isinstance(default_servers, dict):
        raise TypeError("Linear defaults must contain a mcpServers object")
    server = default_servers.get("linear")
    if (
        not isinstance(server, dict)
        or server.get("url") != "https://mcp.linear.app/mcp"
    ):
        raise ValueError(
            "Linear defaults must use the official streamable HTTP endpoint"
        )
    changes: list[tuple[Path, bytes]] = []
    for relative in (".mcp.json", ".pi/mcp.json"):
        path = destination / relative
        original = read_config(path) if path.exists() else {}
        original_servers = original.get("mcpServers", {})
        if not isinstance(original_servers, dict):
            raise TypeError(f"{relative}: mcpServers must be a JSON object")
        config = dict(original)
        servers = dict(original_servers)
        if overlay is not None and (overlay / relative).exists():
            incoming = read_config(overlay / relative)
            incoming_servers = incoming.get("mcpServers", {})
            if not isinstance(incoming_servers, dict):
                raise TypeError(f"overlay {relative}: mcpServers must be a JSON object")
            for name, entry in incoming_servers.items():
                if not isinstance(entry, dict):
                    raise TypeError(f"overlay {relative}: server must be a JSON object")
                if name not in servers:
                    servers[name] = entry
                elif servers[name] != entry:
                    print(
                        f"note: kept existing {relative} server despite overlay conflict"
                    )
            for key, value in incoming.items():
                if key == "mcpServers":
                    continue
                if key not in config:
                    config[key] = value
                elif config[key] != value:
                    print(
                        f"note: kept existing {relative} option despite overlay conflict"
                    )
        if "linear" in servers and servers["linear"] != server:
            print(f"note: kept configured {relative} Linear entry; verify it manually")
        servers.setdefault("linear", server)
        config["mcpServers"] = servers
        if config != original:
            changes.append((path, (json.dumps(config, indent=2) + "\n").encode()))
    relative = ".agents/skills/bmad-linear/SKILL.md"
    path = destination / relative
    skill_path = source / relative
    if overlay is not None and (overlay / relative).exists():
        skill_path = overlay / relative
    skill = skill_path.read_bytes()
    if not path.exists() or path.read_bytes() != skill:
        changes.append((path, skill))
    # Never follow a destination symlink into user-global configuration or another repo.
    for path, _ in changes:
        if not path.resolve().is_relative_to(destination.resolve()):
            raise ValueError(
                f"refusing deployment outside destination: {path.relative_to(destination)}"
            )
    return changes


def deploy(
    source: Path,
    destination: Path,
    *,
    dry_run: bool = False,
    backup_dir: Path | None = None,
    overlay: Path | None = None,
) -> list[Path]:
    """Apply a validated deployment; dry runs create neither files nor backups."""
    changes = deployment_changes(source, destination, overlay=overlay)
    if backup_dir is not None:
        for path, _ in changes:
            backup = backup_dir / path.relative_to(destination)
            if backup.resolve() == path.resolve():
                raise ValueError("backup must not replace its own destination file")
            if not backup.resolve().is_relative_to(backup_dir.resolve()):
                raise ValueError("refusing backup outside the backup directory")
    for path, contents in changes:
        relative = path.relative_to(destination)
        print(f"{'would install' if dry_run else 'installing'} {relative}")
        if dry_run:
            continue
        if backup_dir is not None and path.exists():
            backup = backup_dir / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            # The overlay backup from sync.sh is older and must win if already present.
            if not backup.exists():
                data = path.read_bytes()
                mode = path.stat().st_mode & 0o777
                descriptor = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
                try:
                    with os.fdopen(descriptor, "wb") as output:
                        output.write(data)
                except OSError:
                    backup.unlink(missing_ok=True)
                    raise
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary: str | None = None
        try:
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
                temporary = output.name
                output.write(contents)
            if path.exists():
                os.chmod(temporary, path.stat().st_mode & 0o777)
            os.replace(temporary, path)
            temporary = None
        finally:
            if temporary is not None:
                Path(temporary).unlink(missing_ok=True)
    return [path for path, _ in changes]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--overlay", type=Path)
    args = parser.parse_args()
    if not (args.destination / "_bmad").is_dir():
        parser.error("destination is not a BMAD installation (_bmad/ missing)")
    try:
        deploy(
            args.source,
            args.destination,
            dry_run=args.dry_run,
            backup_dir=args.backup_dir,
            overlay=args.overlay,
        )
    except (ValueError, TypeError, KeyError, OSError) as error:
        # Do not print config values: existing MCP files may contain credentials.
        parser.exit(
            1,
            f"Linear deployment failed: {type(error).__name__}; check MCP file structure and paths\n",
        )


if __name__ == "__main__":
    main()
