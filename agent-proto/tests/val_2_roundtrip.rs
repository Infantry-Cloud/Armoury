//! Acceptance test STORY-1.1 VAL-2 (AC-1, AC-5): agent.proto codegen produces a working prost type.
//!
//! ATDD red phase: locked at contract approval. Task T2 adds `agent-proto` to the Cargo
//! workspace and activates this test by removing the `#[ignore]` line only (the validator
//! treats it as a skip marker, SD-1). Any other edit needs Correct Course.

use agent_proto::v1::Heartbeat;
use prost::Message;

#[test]
#[ignore = "ATDD red phase: Task T2 removes this line"]
fn val_2_generated_message_roundtrip() {
    let sent = Heartbeat {
        agent_id: "val-2-agent".to_owned(),
        ..Default::default()
    };

    let received = Heartbeat::decode(sent.encode_to_vec().as_slice())
        .expect("a Heartbeat encoded by prost decodes again");

    assert_eq!(received, sent);
}
