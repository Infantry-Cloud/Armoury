//! Generates the agent protocol types from `proto/agent/v1` with protox, so no `protoc` is needed.

use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Read at run time: a compile-time `env!` would pin the path of the first checkout to build it.
    let proto_root = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?).join("../proto");
    let agent_proto = proto_root.join("agent/v1/agent.proto");
    println!("cargo:rerun-if-changed={}", proto_root.display());

    let descriptors = protox::compile([&agent_proto], [&proto_root])?;
    tonic_prost_build::compile_fds(descriptors)?;
    Ok(())
}
