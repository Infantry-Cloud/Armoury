# Epic 1 Context: Install, sign in, and the Armoury shell

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Make the start of the first-30-minutes journey real. A SecOps engineer installs the self-hosted control plane with one `helm install`, signs in with a bootstrap admin, and reaches a themed, accessible, keyboard-first shell with an honest empty Posture page. OIDC and the three roles are optional and set through Helm values. The epic also builds the monorepo, the local gate, CI, image builds and the Skaffold dev loop that every later epic depends on. It covers no functional requirements. It delivers the install, access-control, durability and air-gap platform, and sets the UX floor (tokens, shell, accessibility, banned patterns) that later surfaces inherit and must not drop below.

## Stories

- Story 1.1: Monorepo scaffold with an aggregate local gate and CI
- Story 1.2: Install the control plane with one Helm command, durable storage included
- Story 1.3: Sign in with the bootstrap admin
- Story 1.4: Declarative OIDC sign-in and role-based access
- Story 1.5: Design tokens and the three themes
- Story 1.6: App shell, navigation and the empty Posture page
- Story 1.7: Accessibility, message catalogue and responsive baseline
- Story 1.8: Command palette and keyboard map
- Story 1.9: Banned-pattern guards

## Requirements & Constraints

- **Install path is a product gate:** the time from `helm install` to the first posture view must stay under 30 minutes for one engineer. Nothing on the install path may need SSO, a wizard or help from a dev team. OIDC is optional at install and never blocks it.
- **Self-hosted and air-gap capable:** no phone-home. With `airGapped: true` the control plane makes no outbound connections, which a test proves. The air-gap mode is exposed read-only through the API. Fonts and all other assets are bundled locally, with no CDN.
- **Durability:** a single control-plane instance with no HA. Postgres and SeaweedFS use persistent volumes, so deleting the pod loses no data.
- **Access control:** OIDC is configured only through env, Helm values or a config file, never a UI wizard. A bootstrap admin covers first sign-in and IdP outages. The roles are admin, analyst and read-only auditor. A user whose claims map to no role is denied and gets no default role. CI tokens are not a user role.
- **Accessibility:** WCAG 2.2 AA as a contractual floor. Full keyboard operation with visible focus rings and tab order that follows reading order. Polite `aria-live` announcements. Global `prefers-reduced-motion`. State is never shown by colour alone.
- **Platform:** ≥1280px is the primary width. 1024–1279px degrades tolerantly. Below 1024px is best-effort read-only. Web only, last two versions of evergreen browsers.
- **Configurable with smart defaults:** where several valid approaches exist, make the choice a setting with a default, so a default install needs no configuration. Record the default and the alternatives in the story.
- **Dev loop rule:** after Story 1.1, `skaffold dev -p kind` must run and be healthy during every development step. Check changes against the live deployment and with `mise run check`. Story 1.1 is readiness-enabling: Agent Readiness must be ready before Stories 1.2+ start Build.

## Technical Decisions

- **Monorepo:**
  - A Cargo workspace (resolver 3, Rust 2024) holds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1`).
  - `web/` is a SvelteKit SPA using `adapter-static` with SSR off, Tailwind v4, shadcn-svelte and `@xyflow/svelte`.
  - `charts/armoury` is an umbrella chart with `control-plane` and `agent` subcharts.
  - `mise.toml` pins every tool, and tasks are mise file tasks in `mise-tasks/`. All versions are pinned and lockfiles committed; nothing uses `latest`.
- **Gate:**
  - `mise run check` runs rustfmt, `clippy -D warnings`, `cargo nextest`, web lint, `svelte-check`, Vitest and the API drift check.
  - `#[sqlx::test]` runs against `apache/age:release_PG18_1.8.0`, pinned by digest.
  - `mise run e2e` runs Playwright against the Skaffold deployment.
  - CI (`ci.yml`) installs mise with `jdx/mise-action`, pinned by commit, and runs the same tasks. `build.yml` builds the images and chart on every push and pushes them to GHCR by digest on `main`.
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
  - `AGENTS.md`/`CLAUDE.md` states these rules and the dev-loop rule.
- **Frontend:**
  - Server state uses TanStack `svelte-query` over the generated client, and local state uses Svelte 5 runes.
  - Components live with their routes. Only shared shadcn-svelte primitives go in `lib/components/ui`.
  - The palette lives in `lib/command/` and the token maps in `lib/theme/`.
  - Component files are kebab-case.

Sketch of the API shapes (illustrative only; the field names are the ones above):

```json
{"items": [...], "page": {...}}
{"error": {"code": "snake_case_code", "message": "...", "details": {}}}
```

## UX & Interaction Patterns

- **Tokens:**
  - There are three dark themes: Forge (default), High Signal and Gunmetal. There is no light mode and no OS-preference detection.
  - Semantic roles map onto shadcn CSS variables using the exact DESIGN.md values, including `rail-*`, `data-quality`, `data-quality-muted` and `node-inactive-border`. Components use roles only, never raw hex or theme-suffixed variables, and a lint enforces this.
  - Elements that contain text are never shown with opacity below 1; use the muted tokens instead.
  - Contrast tests:
    - AA (4.5:1) for all text roles in Forge and Gunmetal.
    - AAA for High Signal primary text, and ≥7:1 for High Signal muted text.
    - 4.5:1 for `data-quality-muted` and 3:1 for `node-inactive-border` in all three themes.
- **Typography:**
  - Inter Display for numerals and titles, Inter for all UI text, IBM Plex Mono for every identifier. Numerals use `tabular-nums`.
  - Use the DESIGN.md sizes exactly, with no intermediate sizes.
  - Radii: 5/8/9/12/11. Spacing: rail 58, gutter 52, zone gap 48–56, data row 30, stat gap 44.
  - Depth comes from tonal layering and 1px borders. Shadows are used only on overlays.
- **Shell:**
  - A 58px icon rail holds 7 surfaces, with Settings pinned to the bottom. The active item gets a raised tint and a 2px accent indicator. Tooltips show on hover and focus. There is no top nav.
  - Every surface has a page header row with a breadcrumb, the blast-radius search field (opens the palette) and a compact theme switcher (swatch + name).
  - The heading block is left-aligned: eyebrow → title → subtitle (≤620px) → 46×2px accent rule.
  - Empty surfaces show a calm line with no illustrations. The empty Posture page says that no sources are connected yet.
- **Settings:** an in-page left list grouped as Connections, Feeds, Policy, Access, Signals and Personal, with each panel at `/settings/<panel>`. Epic 1 fills these panels: theme picker (live preview, instant apply without reload), read-only auth configuration, users/roles, and the shortcut list.
- **Auditor:** mutation controls are absent from the DOM, not disabled.
- **Loading and errors:** use a layout-mirroring `Skeleton` and show the error envelope's `message`. Never show a bare spinner.
- **Palette:**
  - `⌘K`/`Ctrl+K` opens a shadcn `Command` palette with groups Answers → Navigate → Actions → Recent. Results are announced through `aria-live`.
  - It includes "Switch theme…" with live preview.
  - The no-match copy is "No matches. Try a CVE ID, package@version, or digest."
  - Actions come from one shared action registry, and every shortcut must have a palette entry.
- **Keys:** the bindings are fixed for v1:
  - `g`+`p/b/g/a/f/e` navigates.
  - `?` opens the shortcut map.
  - `Esc` closes the topmost layer.
  - Shortcuts never fire while focus is in a text input.
- **Copy:**
  - Every string comes from an externalised catalogue, with no concatenation and no text in SVG. A lint enforces this.
  - The locked glossary and the lowercase triage statuses are defined once.
  - The tone is calm, built on counts and verbs.
- **Banned patterns, enforced by checks:**
  - in-product notifications or toasts used as alerts; Toast may only confirm the user's own action
  - new-finding badges and celebratory animation
  - an OIDC wizard
  - evidence edit or delete
  - infinite scroll
  - overlays deeper than a drawer plus one dialog, through one shared overlay component
  - hover-only affordances
  - more than one primary button per surface

## Cross-Story Dependencies

- **Story 1.1 comes first.** It provides the gate, the generated API client, Playwright, Dockerfiles and Skaffold. Agent Readiness (INF-12) must pass after it, before any other story starts Build.
- **Story 1.2** needs the 1.1 images and kind profile. Its install, durability and same-origin tests run against `skaffold run -p kind`.
- **Stories 1.3 → 1.4:** 1.4 builds on the 1.3 sessions and the error envelope.
- **Stories 1.5 → 1.6 → 1.8:**
  - 1.5 provides the preference API.
  - 1.6 adds the theme picker and the page header.
  - 1.8 adds palette theme switching and makes the 1.6 header search open the palette.
- **Story 1.7** builds on the 1.6 shell and the 1.1 Playwright setup. Its axe and viewport checks automatically include routes that later stories add.
- **Hooks for later epics:**
  - Posture setup actions and the empty state arrive in Stories 2.2 and 3.2.
  - Blast-radius answers in the palette arrive in Story 6.3.
  - The agent mTLS listener arrives in Story 3.1.
  - Real CI-token routes arrive in Story 11.1 and the pack role-setting route in Story 9.5. Both are covered by the 1.4 route test.
  - Monthly partitioning in the migration Job starts with Story 2.1.
