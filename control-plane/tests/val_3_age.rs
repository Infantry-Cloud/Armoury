//! Acceptance test STORY-1.1 VAL-3 (AC-3, AC-5): `#[sqlx::test]` runs against the digest-pinned
//! `apache/age:release_PG18_1.8.0` image that `mise run check` provides through `DATABASE_URL`.
//!
//! ATDD red phase: this file is locked at contract approval. It has no `#[ignore]` marker
//! because the validator cannot strip Rust markers; it stays inactive until Task T3 adds
//! `control-plane` to the Cargo workspace. Do not edit it without Correct Course.

use sqlx::PgPool;

// Migrations are off on purpose: this check is about the database image, not the schema.
#[sqlx::test(migrations = false)]
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
