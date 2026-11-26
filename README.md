# Armoury

Self-hosted software supply-chain security for Kubernetes fleets: a control plane (Rust, with a
SvelteKit web app on the same origin) and a read-only cluster agent, installed with Helm.

Agents: read `AGENTS.md` first.

## Prerequisites

- [mise](https://mise.jdx.dev). `mise install` provides every other tool at its pinned version
  (Rust, Node, Helm 4, kubectl, Okteto CLI, crane, CodeQL, Renovate, …). No Java, container
  runtime, local cluster or local database is used.
- An Okteto context on the dev cluster, provided outside this repository: you can log in with
  `okteto context use <okteto-url>`, build images, deploy and run tests in your own Okteto
  namespace. `okteto kubeconfig` writes the kube context for that namespace.

## Init

```sh
mise install
cp mise.local.toml.example mise.local.toml   # then fill in the three site values
```

`mise.local.toml` is untracked and holds `ARMOURY_OKTETO_CONTEXT` (your Okteto context),
`ARMOURY_KUBE_CONTEXT` (the kube context that `okteto kubeconfig` writes for your namespace) and
`ARMOURY_NAMESPACE` (your Okteto namespace). Every task passes them explicitly; nothing relies on
your current Okteto or kube context.

## Commands

| Command | What it does |
| --- | --- |
| `mise run dev` | Dev loop: `okteto up` builds both images on Okteto, deploys the chart into your namespace and runs the control plane with `cargo watch`; the UI and API are on `http://localhost:8080`. Keep it running while you work. |
| `mise run check` | The handoff gate. Fast tier: `pins`, `rust`, `test-rust`, `web`, `chart`, `test-tasks`. Cluster tier: `api`, `test-db`, `test-tasks-cluster`, `codeql`. Stops at the first failing step and names it. |
| `mise run check:fast` | Only the fast tier, for iteration. Needs no Okteto or kube context. |
| `mise run check:<step>` | One gate step, for example `mise run check:web`. |
| `mise run e2e` | Playwright smoke test against `http://localhost:8080` (override with `ARMOURY_E2E_BASE_URL`). Fails when nothing is reachable. |
| `mise run gen:api` | Regenerates the Rust server types (openapi-generator in an `okteto test` container) and the TS types from `api/openapi.yaml`. Never edit generated code. |
| `mise run ci` | The CI tiers in CI order: `ci:fast`, `ci:cluster`, `ci:e2e`. Stops at the first failing tier. |
| `mise run ci:e2e` | Deploys the working tree into a fresh `armoury-ci-<suffix>` namespace, prints the namespace and base URL, runs the smoke test with `okteto test` and deletes the namespace (also on failure or Ctrl-C). |
| `mise run renovate` | Renovate dry run: lists every dependency it would keep up to date; changes nothing. |

## CI

GitHub Actions only installs mise and runs one task per job (`.github/workflows/`):

- `ci.yml`: `fast` (`ci:fast`, hosted, every event); `cluster` (`ci:cluster`) and `e2e`
  (`ci:e2e`; for a pull request, the Okteto preview `pr-<n>`) on ARC runners for pushes and
  same-repository pull requests only; `ci-gate` always runs and fails unless every job succeeded.
  A fork pull request therefore never passes `ci-gate`: a maintainer pushes its commits to a
  branch of this repository to run the cluster tiers.
- `build.yml`: `ci:build` on every push (images with `okteto build`, chart with `helm package`);
  `ci:publish` on `main` copies both images by digest to `ghcr.io/<owner>/armoury-control-plane`
  and `ghcr.io/<owner>/armoury-agent`.
- `preview-cleanup.yml`: destroys the preview of a closed same-repository pull request.
- `renovate.yml`: weekly and on demand, Renovate opens pull requests that keep every pin exact.

Repository setup (outside this repository): an ARC scale set named `armoury-arc` for the
Infantry-Cloud organisation (GitOps `devops/arc`) whose runners provide `ARMOURY_OKTETO_CONTEXT`,
`ARMOURY_KUBE_CONTEXT`, `ARMOURY_NAMESPACE` and an Okteto identity; Okteto access to the repository
for previews; the `RENOVATE_TOKEN` secret; workflow approval required for all external
contributors on every public Infantry-Cloud repository, because any of them can use these runners.

## Licence

Apache-2.0, see `LICENSE`.
