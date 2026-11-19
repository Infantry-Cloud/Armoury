//! Cluster-agent entrypoint: wiring only. Watchers and the reporter arrive in Epic 3.

use anyhow::Context;
use k8s_openapi::apimachinery::pkg::version::Info;
use tracing_subscriber::EnvFilter;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .json()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .init();

    let client = kube::Client::try_default()
        .await
        .context("loading the in-cluster Kubernetes config")?;
    let cluster: Info = client
        .apiserver_version()
        .await
        .context("reading the Kubernetes API version")?;
    tracing::info!(version = env!("CARGO_PKG_VERSION"), kubernetes = %cluster.git_version, "armoury-agent started");

    let mut terminate = tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())?;
    tokio::select! {
        result = tokio::signal::ctrl_c() => result?,
        _ = terminate.recv() => {}
    }
    Ok(())
}
