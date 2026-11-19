//! Agent to control-plane protocol types, generated from `proto/agent/v1/agent.proto`.

/// Version 1 of the agent protocol (`armoury.agent.v1`).
pub mod v1 {
    include!(concat!(env!("OUT_DIR"), "/armoury.agent.v1.rs"));
}
