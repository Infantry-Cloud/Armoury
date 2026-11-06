//! Acceptance test STORY-1.1 VAL-2 (AC-1, AC-5): agent.proto codegen produces a working prost type.
//!
//! ATDD red phase: this file is locked at contract approval. It has no `#[ignore]` marker
//! because the validator cannot strip Rust markers; it stays inactive until Task T2 adds
//! `agent-proto` to the Cargo workspace. Do not edit it without Correct Course.

use agent_proto::v1::Heartbeat;
use prost::Message;

#[test]
fn val_2_generated_message_roundtrip() {
    let sent = Heartbeat {
        agent_id: "val-2-agent".to_owned(),
        ..Default::default()
    };

    let received = Heartbeat::decode(sent.encode_to_vec().as_slice())
        .expect("a Heartbeat encoded by prost decodes again");

    assert_eq!(received, sent);
}
