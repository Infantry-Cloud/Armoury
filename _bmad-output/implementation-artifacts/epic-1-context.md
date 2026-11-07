# Epic 1 Context: Install, sign in, and the Armoury shell

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Make the start of the first-30-minutes journey real. A SecOps engineer installs the self-hosted control plane with one `helm install`, signs in with a bootstrap admin, and reaches an accessible, keyboard-first shell — labelled black sidebar, Light (default) and Dark themes — with an honest empty Home page. OIDC and the three roles are optional and set through Helm values. The epic also builds the monorepo, the local gate, CI, image builds and the Skaffold dev loop that every later epic depends on. It covers no functional requirements. It delivers the install, access-control, durability and air-gap platform, and sets the UX floor (tokens, shell, accessibility, banned patterns) that later surfaces inherit and must not drop below.

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

- **Install path is a product gate:** the time from `helm install` to the first posture view must stay under 30 minutes for one engineer. Nothing on the install path may need SSO, a wizard or help from a dev team. OIDC is optional at install and never blocks it.
- **Self-hosted and air-gap capable:** no phone-home. With `airGapped: true` the control plane makes no outbound connections, which a test proves. The air-gap mode is exposed read-only through the API. Fonts and all other assets are bundled locally, with no CDN.
- **Durability:** a single control-plane instance with no HA. Postgres and SeaweedFS use persistent volumes, so deleting the pod loses no data.
- **Access control:** OIDC is configured only through env, Helm values or a config file, never a UI wizard. A bootstrap admin covers first sign-in and IdP outages. The roles are admin, analyst and read-only auditor. A user whose claims map to no role is denied and gets no default role. CI tokens are not a user role.
- **Accessibility:** WCAG 2.2 AA as a contractual floor. Full keyboard operation with visible focus rings and tab order that follows reading order. Polite `aria-live` announcements. Global `prefers-reduced-motion`. State is never shown by colour alone. Single-key shortcuts can be turned off (2.1.4). Field edges are ≥3:1 at rest (1.4.11). Content reflows at 400% zoom and 200% text.
- **Platform:** ≥1280px: full sidebar and three columns. 1024–1279px: icon rail, list and detail side by side. Below 1024px: icon rail, list and detail stacked with a Back link, fully operable. Web only, last two versions of evergreen browsers.
- **Configurable with smart defaults:** where several valid approaches exist, make the choice a setting with a default, so a default install needs no configuration. Record the default and the alternatives in the story.
- **Dev loop rule:** after Story 1.1, `mise run dev` (Skaffold on the dev cluster) must run and be healthy during every development step. Check changes against the live deployment and with `mise run check`. Story 1.1 is readiness-enabling: Agent Readiness must be ready before Stories 1.2+ start Build.

## Technical Decisions

- **Monorepo:**
  - A Cargo workspace (resolver 3, Rust 2024) holds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1`).
  - `web/` is a SvelteKit SPA using `adapter-static` with SSR off, Tailwind v4, shadcn-svelte and `@xyflow/svelte`.
  - `charts/armoury` is an umbrella chart with `control-plane` and `agent` subcharts.
  - `mise.toml` pins every tool, and tasks are mise file tasks in `mise-tasks/`. All versions are pinned and lockfiles committed; nothing uses `latest`.
- **Gate:**
  - `mise run check` runs rustfmt, `clippy -D warnings`, `cargo nextest`, web lint, `svelte-check`, Vitest and the API drift check.
  - `#[sqlx::test]` runs against `apache/age:release_PG18_1.8.0`, pinned by digest, as a Pod in the dev cluster. No database, image build or cluster runs on the workstation.
  - `mise run e2e` runs Playwright against the Skaffold deployment.
  - CI (`ci.yml`) installs mise with `jdx/mise-action`, pinned by commit, and runs the same tasks. Fork pull requests run only the fast tier on GitHub-hosted runners; the full gate and e2e run on ARC runners in the dev cluster. `build.yml` builds the images and chart on every push and pushes them to GHCR by digest on `main`.
- **Images:** multi-stage Dockerfiles with base images pinned by digest. The control-plane image holds `armoury` and the SPA. The agent image holds only `armoury-agent`, with no scanners. The dev profile uses a debug build and a cached dependency layer (e.g. `cargo-chef`), with a `ponytail:` note that a remote build cache is the upgrade path.
- **OpenAPI-first:**
  - `api/openapi.yaml` is the contract. `mise run gen:api` generates the Rust server types with `openapi-generator` (rust-axum, run from its pinned container image so no local Java is needed) and the TS client with `openapi-typescript` + `openapi-fetch`.
  - Generated code is never hand-edited, and drift fails the check. The fallback is code-first `utoipa` with a spec-diff check.
- **API conventions:** see the sketch after this list.
  - Paths are `/api/v1/<plural-noun>`. JSON and query params use snake_case.
  - Resources are returned unwrapped. Lists use `{items, page}` with cursor pagination.
  - Errors use the envelope `{error:{code,message,details}}`.
  - IDs are UUIDv7. Timestamps are RFC 3339 UTC. Custom headers are `X-Armoury-*`.
- **RBAC:**
  - Every operation declares `x-armoury-role: admin|analyst|auditor`, the minimum role. The middleware reads it, and a spec test fails if it is missing.
  - `x-armoury-role-setting: <setting>` also admits the next lower role when that setting is true.
  - `x-armoury-ci-token: true` marks routes that accept `Authorization: Bearer` CI tokens. A CI token gets 403 on every other route, and a session cookie never counts as a CI token.
  - A route test calls every route with every role and with a CI-token caller.
- **Auth and sessions:**
  - OIDC code flow uses the `openidconnect` crate. Sessions use an httpOnly, Secure, SameSite cookie, and no token is ever kept in JS-accessible storage.
  - The `sessions` table stores only a hash of the random ID held in the cookie, so sessions survive a restart. Idle and maximum lifetimes are Helm values (defaults 8 h and 24 h).
  - Sign-in is rate-limited (defaults: 5 failures per username in 15 min, then a 15 min block; 20 attempts per IP in 15 min).
  - `user_preferences` is keyed by OIDC issuer + `sub`, or a fixed bootstrap-admin ID, and served by `GET`/`PUT /api/v1/me/preferences`.
  - Both tables are marked "not evidence".
  - `GET /api/v1/auth/config` returns the resolved configuration with secrets redacted. There is no API to change it.
- **Data and queue:**
  - The datastore is PostgreSQL 18 + Apache AGE 1.8, bundled and pinned by digest. External Postgres-AGE and S3 are opt-in.
  - There are two logins. `armoury_owner` owns every table and is used only by the migration Job. `armoury_app` owns nothing and is the only login the control plane uses. Each password is in its own Secret, and the control-plane pod mounts only the app Secret.
  - The migration Job (`armoury migrate`) is a Helm post-install/pre-upgrade hook. It runs River migrations, then forward-only `sqlx` migrations, creates the AGE graph and grants rights, and retries the DB connection for up to 10 min.
  - The control plane stays not-ready until the schema reaches its expected version. The documented install must not use `--wait` or `--atomic`.
  - The job queue is `riverqueue =0.5.0`, which needs sqlx 0.9 and `jiff`, with transactional enqueue. If the commit/rollback test cannot pass, switch to `graphile_worker` within Story 1.2.
- **Chart:** the control plane serves the SPA and `/api/v1/*` from the same origin. It has a separate agent port with its own Service: `LoadBalancer` by default, `NodePort`, or ingress with TLS passthrough. An ingress that ends TLS is unsupported, and the docs must say so. The listener itself arrives in Epic 3. Chart NOTES explain how to get the bootstrap credential without printing it.
- **Code rules (Locality of Behaviour):**
  - Organise by capability (`auth`, `postgres`, `blob`, `httpapi` and so on). Use at most 3 layers and wire everything in `main.rs` only.
  - No globals or singletons, no `utils/`/`helpers/`/`common/`, and traits only at the third occurrence. One `thiserror` enum per capability, and `anyhow` only in `main`.
  - No `unwrap`/`expect` outside tests and startup, and no `unsafe`. Files are 100–400 lines, each opening with a one-line purpose comment.
  - Logs are structured `tracing` JSON and never contain credentials.
  - `AGENTS.md` states these rules and the dev-loop rule. There is no `CLAUDE.md`.
- **Frontend:**
  - Server state uses TanStack `svelte-query` over the generated client, and local state uses Svelte 5 runes.
  - Components live with their routes. Only shared shadcn-svelte primitives go in `lib/components/ui`.
  - The palette lives in `lib/command/`, the token maps in `lib/theme/`, and the brand-layer components every surface shares (shell, list row, markers, status chip, inline error, code block) in `lib/design/`.
  - Component files are kebab-case.

Sketch of the API shapes (illustrative only; the field names are the ones above):

```json
{"items": [...], "page": {...}}
{"error": {"code": "snake_case_code", "message": "...", "details": {}}}
```

## UX & Interaction Patterns

- **Tokens:**
  - Two themes over the same roles: Light (default, unsuffixed tokens) and Dark (`-dark`); new users get Light; no OS-preference detection.
  - Roles map onto shadcn variables per the DESIGN.md "shadcn mapping" table, plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`; `print-*` tokens feed only Typst. Components use roles only, never raw hex or theme-suffixed variables, and a lint enforces this.
  - No opacity below 1 on elements with text, except disabled controls at 0.45.
  - Contrast tests:
    - AA 4.5:1 for every text pair in the DESIGN.md Contrast table, in both themes (lowest 4.9:1), including `dq` and `dq-muted`.
    - ≥3:1 for `field-border` and the focus ring; markers below 3:1 only beside a word.
- **Typography:**
  - IBM Plex Sans for everything; Plex Sans Bold Italic for the wordmark only; Plex Mono only for IDs, fingerprints, commands and keys; all self-hosted (OFL). Numerals use `tabular-nums` in data.
  - Nine sizes 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40, plus the 22px wordmark; weights 400/500/600. Sentence case; uppercase only on button labels; no eyebrows.
  - Radii 3 / 4 / 6 / 10, pill, full. Layout: sidebar 252, list column 376 / 500 / 420, gutter 32, detail cell 30 × 34, rows ≈78 / 72px; one density.
  - Depth is tone + 1px rules; the only shadow is the ⌘K dialog.
- **Shell:**
  - A 252px black sidebar: wordmark, "Search or jump to… ⌘K" field, Home · Software · Issues · Exposure · Reports, a divider, Settings · Help, and the user menu (name, role, Personal settings, Sign out) at the foot; the active item is lime. The Issues badge (Needs-attention count) arrives in Story 2.10. Help opens a placeholder until its screen is designed.
  - No top nav and no page header. Three-column master-detail; page title = sidebar label + one summary line.
  - Below 1280px the sidebar becomes an icon rail; below 1024px list and detail stack with a Back link.
  - Empty surfaces show a calm line with no illustrations. The empty Home says that no sources are connected yet.
- **Settings:** a panel list in the list column, grouped as Connections, Sources, Policy, Access, Signals and Personal, with each panel at `/settings/<panel>`. Epic 1 fills Personal (the Light/Dark theme switch, instant apply; the shortcut list; the single-key shortcut switch) and Access (read-only auth configuration, users/roles).
- **Auditor:** mutation controls are absent from the DOM, not disabled.
- **Loading and errors:** use a layout-mirroring `Skeleton` and show the error envelope's `message`. Never show a bare spinner. A failed save or start shows an inline error line with Try again in the panel where it happened, never a toast.
- **Palette:**
  - `⌘K`/`Ctrl+K` (and the sidebar search field) opens a 660px shadcn `Command` dialog with groups Issues · Software · Exposure · Actions (Recent is not drawn); it traps focus, dims the page and returns focus on `Esc`. Results are announced through polite `aria-live`.
  - It includes "Switch theme…" (Light / Dark).
  - The no-match copy is "No matches. Try a CVE ID, package@version or fingerprint."
  - Actions come from one shared action registry, and every shortcut must have a palette entry.
- **Keys:** the bindings are fixed for v1:
  - `g` + a surface letter navigates (letters set by UX before Story 1.8 Build, EXPERIENCE Open item 13); `J`/`K` move, `/` focuses search, `⌘↵` saves and goes to the next, `x` exports.
  - `?` opens the shortcut map.
  - `Esc` closes the topmost layer.
  - Single-key shortcuts never fire while focus is in a text field and can be turned off in Settings → Personal; `⌘K` and `⌘↵` stay on.
- **Copy:**
  - Every string comes from an externalised catalogue, with no concatenation and no text in SVG. A lint enforces this.
  - The plain-label glossary (plain label first, technical term small and grey) and the five review statuses (Not reviewed yet, Not impacted, Fix planned, Mitigated, Risk accepted) are defined once; British English; retired labels fail a lint.
  - The tone is calm, built on counts and verbs.
- **Banned patterns, enforced by checks:**
  - in-product notifications and toasts (as alerts or for save results)
  - new-finding badges (the Needs-attention badge is allowed), celebratory animation, a Compact density toggle
  - an OIDC wizard
  - evidence edit or delete
  - infinite scroll
  - any modal besides the ⌘K dialog, and any drawer (one shared overlay component)
  - hover-only affordances
  - more than one lime primary action per view; lime outside its agreed jobs; red anywhere

## Cross-Story Dependencies

- **Story 1.1 comes first.** It provides the gate, the generated API client, Playwright, Dockerfiles and Skaffold. Agent Readiness (INF-12) must pass after it, before any other story starts Build.
- **Story 1.2** needs the 1.1 images and the Skaffold `ci` profile. Its install, durability and same-origin tests run in a fresh dev-cluster namespace.
- **Stories 1.3 → 1.4:** 1.4 builds on the 1.3 sessions and the error envelope.
- **Stories 1.5 → 1.6 → 1.8:**
  - 1.5 provides the preference API.
  - 1.6 adds the sidebar, the user menu and the Settings → Personal theme switch.
  - 1.8 adds palette theme switching, makes the 1.6 sidebar search field open the palette, and adds the single-key shortcut switch.
- **Story 1.7** builds on the 1.6 shell and the 1.1 Playwright setup. Its axe and viewport checks automatically include routes that later stories add.
- **Hooks for later epics:**
  - Home setup actions and the empty state arrive in Stories 2.2 and 3.2; the Issues badge arrives in Story 2.10.
  - Exposure answers in the palette arrive in Story 6.3.
  - The agent mTLS listener arrives in Story 3.1.
  - Real CI-token routes arrive in Story 11.1 and the pack role-setting route in Story 9.5. Both are covered by the 1.4 route test.
  - Monthly partitioning in the migration Job starts with Story 2.1.
