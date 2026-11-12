# Epic 1 Context: Install, sign in, and the Armoury shell

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Give a SecOps engineer a working, self-hosted Armoury in minutes: one `helm install` brings up the control plane with durable bundled storage, the engineer signs in with a bootstrap admin (OIDC and the three roles optional, configured only through Helm values), and lands in the Armoury shell — labelled black sidebar, ⌘K palette, Light (default) and Dark themes — on an honest empty Home page. The epic delivers no product features (no FRs); it lays the monorepo, toolchain, CI, dev loop, API spine, auth/RBAC and the UI floor (tokens, accessibility, copy catalogue, banned-pattern guards) that every later epic inherits. Story 1.1 is readiness-enabling: Agent Readiness runs after it and must pass before Stories 1.2+ start Build.

## Stories

- Story 1.1: Monorepo scaffold with an aggregate local gate and CI
- Story 1.2: Install the control plane with one Helm command, durable storage included
- Story 1.3: Sign in with the bootstrap admin
- Story 1.4: Declarative OIDC sign-in and role-based access
- Story 1.5: Design tokens and the Light and Dark themes
- Story 1.6: App shell, sidebar navigation and the empty Home page
- Story 1.7: Accessibility, message catalogue and responsive baseline
- Story 1.8: Command palette and keyboard map
- Story 1.9: Banned-pattern guards

## Requirements & Constraints

- **Install path is sacred:** self-hosted Helm chart into an existing cluster; one command with default values and no required configuration; fully air-gap capable, no phone-home, nothing silently needing internet. Anything that would break "install to first posture view in < 30 min" doesn't ship in the install path.
- **Durability:** single-instance control plane (no HA), but losing the pod never loses stored data — Postgres and the object store sit on persistent volumes.
- **Access control:** OIDC configured declaratively only (Helm values/env/config, never a UI wizard, no API to change it); OIDC optional at install; bootstrap admin always works, including during IdP outage; roles admin / analyst / auditor; unmapped claims are denied, never defaulted. Scoped CI tokens are not a role.
- **Options with smart defaults:** where several valid approaches exist (session lifetimes, rate limits, agent port exposure), make them Helm values with a default so a default install needs nothing.
- **Dev workflow:** after Story 1.1, every development step runs with `mise run dev` (`okteto up` dev container) live; changes are verified against that deployment plus `mise run check`. Fix an unhealthy loop before writing code.
- **UI floor:** WCAG 2.2 AA in both themes, full keyboard operability, reflow to 400% zoom, reduced-motion support, all copy externalised in British English, retired labels banned — enforced by automated checks that later routes inherit automatically.

## Technical Decisions

- **Monorepo:** Cargo workspace (resolver 3, Rust 2024) with `control-plane` (binary `armoury`), `agent` (`armoury-agent`), `agent-proto` (tonic/prost from `proto/agent/v1`); `web/` SvelteKit + Svelte 5 + Tailwind v4 + shadcn-svelte + `@xyflow/svelte`, `adapter-static`, SSR off; `charts/armoury` umbrella with control-plane and agent subcharts. `mise.toml` pins every tool; tasks are mise file tasks in `mise-tasks/` (`check`, `ci`, `e2e`, `gen:api`, `dev`, `renovate`). Lockfiles committed, nothing floating.
- **Gate & CI:** `mise run check` = rustfmt, `clippy -D warnings`, `cargo nextest` (incl. `#[sqlx::test]` against `apache/age:release_PG18_1.8.0` pinned by digest, run as a Pod in the Okteto namespace — no local DB), web lint, `svelte-check`, Vitest, API-drift check, CodeQL. Every CI step is a mise task: workflows only install mise (`jdx/mise-action` pinned by commit) and call `mise run ci:<tier>`, and `mise run ci` runs the same pipeline locally. Forks get only `ci:fast` on hosted runners; `ci:cluster`, `ci:e2e` (Okteto preview per PR) and `ci:build` run on ARC runners in a separate runner cluster that reaches the dev cluster through Okteto. `ci:publish` copies both images to GHCR by digest on `main`. Renovate runs as `mise run renovate` (dry run by default).
- **Images & dev loop:** multi-stage Dockerfiles, bases pinned by digest; control-plane image = `armoury` + SPA build; agent image has no scanner tools. Okteto (`okteto.yaml`; installed and operated outside this repository) builds both images on its BuildKit into its registry, deploys the chart with images by digest to the developer's namespace, and `okteto up` runs a control-plane dev container with file sync, `cargo watch` and `localhost:8080`. `ci:e2e` deploys a preview (CI) or a fresh namespace (local). No local container runtime or cluster. Debug profile, `cargo-chef` layer for images, persistent cargo cache in the dev container; `ponytail:` note for slow rebuilds. DevSpace is reconsidered after Epic 1.
- **Data & queue:** Postgres 18 + AGE 1.8 is the source of truth; SeaweedFS for blobs; external DB/S3 opt-in (docs state exact rights; migration fails clearly if missing). Two logins: `armoury_owner` (owns tables; used only by migration Job/maintenance) and `armoury_app` (control-plane login, the only Secret it mounts). Migration Job (`armoury migrate`, post-install/pre-upgrade hook, retries DB up to 10 min) runs River migrations, then forward-only `sqlx` migrations, then creates the AGE graph and grants. Control plane is not-ready until schema version is current. Documented install must not use `--wait`/`--atomic`. Jobs via `riverqueue =0.5.0` (needs `sqlx` 0.9 + `jiff`) with transactional enqueue; if the enqueue/rollback proof fails, switch to `graphile_worker` in Story 1.2.
- **API spine:** `api/openapi.yaml` is the contract; Rust server types via `openapi-generator` (pinned container, no local Java; fallback code-first `utoipa` with spec-diff check), TS client via `openapi-typescript` + `openapi-fetch`; generated code never hand-edited. Conventions: `/api/v1/<plural-noun>`, snake_case JSON, unwrapped resources, `{items, page}` cursor lists, `{error:{code,message,details}}` envelope, UUIDv7, RFC 3339 UTC, `X-Armoury-*` headers. SPA and API served same-origin by the control plane.
- **Auth & RBAC:** OIDC code flow (`openidconnect`); httpOnly Secure SameSite cookie, no tokens in JS. Sessions in Postgres `sessions` (cookie holds random ID; table stores its hash; survive restart; sign-out deletes row; 8 h idle / 24 h max defaults). Sign-in rate limits: 5 fails per username per 15 min → 15 min block; 20 tries per IP per 15 min. Every operation declares `x-armoury-role` (spec test fails without it); optional `x-armoury-role-setting` opens a route to the next lower role; `x-armoury-ci-token: true` marks routes a Bearer CI token may call (403 elsewhere; cookies never count). `GET /api/v1/auth/config` returns resolved config, secrets redacted.
- **Preferences:** `user_preferences` keyed by OIDC issuer + `sub` (fixed ID for bootstrap admin) via `GET`/`PUT /api/v1/me/preferences` — theme (`light` default | `dark`) and single-key-shortcuts switch (default on). Sessions and preferences are marked "not evidence".
- **Air gap & agent port:** `airGapped: true` means zero outbound connections (prove with an egress test on a NetworkPolicy-enforcing CNI) and is exposed read-only via the API. The chart renders a separate agent port/Service (`LoadBalancer` default, `NodePort`, or TLS-passthrough ingress — TLS-terminating ingress unsupported; listener arrives in Epic 3).
- **Code rules:** Locality of Behaviour (module-by-capability, max 3 layers, wiring only in `main.rs`, no globals or `utils/`), recorded in `AGENTS.md` (no `CLAUDE.md`) with the dev-loop rule; `tracing` JSON logs never contain credentials.
- **Frontend:** svelte-query over the generated client for server state, Svelte 5 runes for local state, surface components co-located with routes; shadcn primitives in `lib/components/ui`, brand-layer shared components in `lib/design/`, palette in `lib/command/`, tokens/fonts in `lib/theme/`. API enums (e.g. triage statuses) stay locked; UI labels map from them in one place in the message catalogue.

## UX & Interaction Patterns

- **Tokens/themes:** semantic roles mapped onto shadcn CSS variables with exact DESIGN.md values, Light (unsuffixed) and Dark (`-dark`), plus `--paper`, `--dq`, `--dq-muted`, `--dq-wash`; components never use raw hex or theme-suffixed vars. Theme switches instantly, persists server-side, new users Light, no OS-preference detection. `print-*` tokens are Typst-only. No red anywhere; lime only for active nav, one primary per view and agreed exceptions.
- **Type/shape:** self-hosted IBM Plex Sans (variable) + Bold Italic (22px wordmark only) + Plex Mono 400 (IDs, commands, keys); nine sizes only (12·13·14·15·17·20·24·30·40), weights 400/500/600, `tabular-nums` in data, sentence case. One density; flat tonal depth with 1px rules; the only shadow is the ⌘K dialog; opacity on text only for disabled controls (0.45). Contrast AA checked automatically (field edges and focus ring ≥ 3:1).
- **Shell:** 252px black sidebar — wordmark, "Search or jump to… ⌘K", Home · Software · Issues · Exposure · Reports, divider, Settings · Help, user menu (avatar, name, role → Personal settings, Sign out) at the foot. No top nav/page header; each surface = title equal to its nav label + one summary line, three-column master-detail. Empty surfaces show a calm "nothing here yet" line. Home pre-setup states no sources are connected (setup actions arrive in Epics 2–3). Settings = panel list (Connections, Sources, Policy, Access, Signals, Personal), one route per panel; this epic fills Personal and Access. Help opens a placeholder.
- **Roles in UI:** auditor mutation controls are absent from the DOM, not disabled.
- **Loading/errors:** layout-mirroring skeletons and the envelope `message` in plain words; never bare spinners.
- **Responsive:** ≥1280 full sidebar; 1024–1279 icon rail with list/detail side by side; <1024 icon rail with stacked list/detail and a Back link at the same URL. No horizontal page scroll (test at 1440/1100/900/320px and 200% text).
- **⌘K & keyboard:** shadcn `Command` in a 660px dialog, groups Issues · Software · Exposure · Actions, focus-trapped, returns focus on `Esc`, never self-navigates, polite announcements, fixed no-match copy; one action registry that later stories register into (every shortcut must have a palette entry). Single-key shortcuts only outside text fields and switchable off; `⌘K`/`⌘↵` always on; `?` opens the palette's Keyboard shortcuts view; no custom bindings.
- **Banned patterns:** one modal only (⌘K), no drawers, no toasts, no second lime primary, no compact density, no data-quality grade in list rows, no celebratory animation — all lint/test-enforced.

## Cross-Story Dependencies

- 1.1 precedes everything and gates Agent Readiness; 1.2 depends on 1.1's `mise run ci:e2e` (Okteto preview or namespace) for install/durability/egress tests against real images.
- 1.3 needs the database from 1.2; 1.4 extends 1.3's sessions with OIDC and RBAC middleware (test-only routes prove role-setting and CI-token paths; Epics 9 and 11 add real ones).
- 1.5's preferences API feeds 1.6's theme picker and 1.8's shortcut switch; 1.7 and 1.9 checks apply to 1.6's shell and auto-cover all later routes.
- Open before Story 1.8 Build: `g`-letters for renamed surfaces, new meanings for `t`/`e`, and the Keyboard shortcuts view layout must be set in the UX spec. Exposure routing from ⌘K activates once Epic 6 lands.
