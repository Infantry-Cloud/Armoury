# Control-plane image: the `armoury` binary and the web app build. Build context: repository root.
# Targets: `dev` (the `okteto up` dev container) and the default runtime image (last stage).
# ponytail: slow Rust rebuilds are the ceiling; cargo-chef caches the dependency layer and the dev
# container keeps a persistent cargo cache. Upgrade path: a remote build cache shared by Okteto and CI.

FROM docker.io/library/rust:1.100.0-bookworm@sha256:ade39a710ef85f3506cffcfec3e8a24ba090badef1dff2fb798f71d878833fea AS chef
RUN cargo install cargo-chef --version 0.1.78 --locked
WORKDIR /src

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS rust-build
ARG CARGO_PROFILE=release
COPY --from=planner /src/recipe.json recipe.json
RUN cargo chef cook --profile "$CARGO_PROFILE" --locked --package armoury --recipe-path recipe.json
COPY . .
RUN cargo build --profile "$CARGO_PROFILE" --locked --package armoury \
  && cp "target/$([ "$CARGO_PROFILE" = dev ] && echo debug || echo "$CARGO_PROFILE")/armoury" /armoury

FROM docker.io/library/node:26.13.1-bookworm-slim@sha256:5df79989ed685e09f0a98019db4cebfb22fb9df1a53c0161664a011f7ff6b0f1 AS web-build
WORKDIR /src/web
COPY web/package.json web/package-lock.json web/.npmrc ./
RUN npm ci --no-audit --no-fund
COPY web/ ./
RUN npm run build

# Dev container for `mise run dev`: debug profile, `cargo watch`, source synced to /usr/src/armoury.
FROM chef AS dev
RUN cargo install cargo-watch --version 8.5.3 --locked
COPY --from=web-build /src/web/build /usr/share/armoury/web
ENV CARGO_TARGET_DIR=/var/cache/armoury/target
WORKDIR /usr/src/armoury
EXPOSE 8080
CMD ["cargo", "watch", "--why", "--watch", "control-plane", "--watch", "Cargo.toml", "--watch", "Cargo.lock", "-x", "run --locked --package armoury"]

FROM gcr.io/distroless/cc-debian12:nonroot@sha256:9dac0a79194e45a7da0158a9c6da57b217585af0786db3845d1f0ec1a0dd182f
COPY --from=rust-build /armoury /usr/local/bin/armoury
COPY --from=web-build /src/web/build /usr/share/armoury/web
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/armoury"]
