# Agent image: only the `armoury-agent` binary on distroless, non-root; no scanner tools (NFR12).
# Build context: repository root.
# ponytail: slow Rust rebuilds are the ceiling; cargo-chef caches the dependency layer.
# Upgrade path: a remote build cache shared by Okteto and CI.

FROM docker.io/library/rust:1.100.0-bookworm@sha256:ade39a710ef85f3506cffcfec3e8a24ba090badef1dff2fb798f71d878833fea AS chef
RUN cargo install cargo-chef --version 0.1.78 --locked
WORKDIR /src

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS rust-build
ARG CARGO_PROFILE=release
COPY --from=planner /src/recipe.json recipe.json
RUN cargo chef cook --profile "$CARGO_PROFILE" --locked --package armoury-agent --recipe-path recipe.json
COPY . .
RUN cargo build --profile "$CARGO_PROFILE" --locked --package armoury-agent \
  && cp "target/$([ "$CARGO_PROFILE" = dev ] && echo debug || echo "$CARGO_PROFILE")/armoury-agent" /armoury-agent

FROM gcr.io/distroless/cc-debian12:nonroot@sha256:9dac0a79194e45a7da0158a9c6da57b217585af0786db3845d1f0ec1a0dd182f
COPY --from=rust-build /armoury-agent /usr/local/bin/armoury-agent
ENTRYPOINT ["/usr/local/bin/armoury-agent"]
