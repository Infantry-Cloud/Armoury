//! Acceptance test STORY-1.1 VAL-3 (AC-3, AC-5): `#[sqlx::test]` runs in the `test-db` gate step
//! against the digest-pinned `apache/age:release_PG18_1.8.0` Pod in the dev cluster, which the
//! step provides through `DATABASE_URL`. It belongs to the database group, so `test-rust` skips it.
//!
//! ATDD red phase: locked at contract approval. Task T3 adds `control-plane` to the Cargo
//! workspace and activates this test by removing the `#[ignore]` line only (the validator
//! treats it as a skip marker, SD-1). Any other edit needs Correct Course.

use sqlx::PgPool;

// Migrations are off on purpose: this check is about the database image, not the schema.
#[sqlx::test(migrations = false)]
#[ignore = "ATDD red phase: Task T3 removes this line"]
async fn val_3_age_extension_is_available(pool: PgPool) -> sqlx::Result<()> {
    sqlx::query("CREATE EXTENSION IF NOT EXISTS age")
        .execute(&pool)
        .await?;

    let version: String =
        sqlx::query_scalar("SELECT extversion FROM pg_extension WHERE extname = 'age'")
            .fetch_one(&pool)
            .await?;

    assert_eq!(version, "1.8.0");
    Ok(())
}
