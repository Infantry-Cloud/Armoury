# VAL-11: injected defect, preview and fork approval (recorded 2026-11-27T05:48:49Z)

Defect: change `oltopmwo` (`597687d6`, bookmark `val-11-defect`), `agent/src/main.rs:27` `Ok(  ())` (unformatted Rust). Never merged.

| Check | Run | Result |
| --- | --- | --- |
| Local `mise run ci` | `val-11-local-ci-defect.log` | exit 1; `check: FAILED at step 'rust'`, `ci: FAILED at tier ci:fast` |
| `ci.yml` pull_request | https://github.com/Infantry-Cloud/Armoury/actions/runs/45939500209 | `fast` and `cluster` failed at step `rust` (Diff in agent/src/main.rs:27); `e2e` success; `ci-gate` failure (`not successful: fast, cluster`) |
| `ci.yml` push | https://github.com/Infantry-Cloud/Armoury/actions/runs/45939485587 | same as above |
| Preview while open | PR https://github.com/Infantry-Cloud/Armoury/pull/1, `e2e` job | `ci:e2e: deploying preview pr-1 from branch val-11-defect`, smoke test 1 passed; `okteto preview list`: `pr-1 global ... val-11-defect` |
| Preview after close | https://github.com/Infantry-Cloud/Armoury/actions/runs/45942171669 | `preview-destroy` success; `okteto preview list`: "There are no previews" |
| Fork approval setting | `GET repos/Infantry-Cloud/Armoury/actions/permissions/fork-pr-contributor-approval` | `all_external_contributors` |

The same defect fails at the same step (`rust`) in `mise run ci` and in CI.
