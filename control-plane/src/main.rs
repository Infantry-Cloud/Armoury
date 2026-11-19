//! Control-plane entrypoint: wiring only (configuration, logging, HTTP server).

mod httpapi;

use std::{net::SocketAddr, path::PathBuf};

use anyhow::Context;
use tracing_subscriber::EnvFilter;

/// UI and API share one origin on this port.
const LISTEN_ADDR: SocketAddr =
    SocketAddr::new(std::net::IpAddr::V4(std::net::Ipv4Addr::UNSPECIFIED), 8080);
/// Where the control-plane image puts the web app build.
const DEFAULT_WEB_ROOT: &str = "/usr/share/armoury/web";

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .json()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .init();

    let web_root = std::env::var_os("ARMOURY_WEB_ROOT")
        .map_or_else(|| PathBuf::from(DEFAULT_WEB_ROOT), PathBuf::from);
    let listener = tokio::net::TcpListener::bind(LISTEN_ADDR)
        .await
        .with_context(|| format!("binding {LISTEN_ADDR}"))?;
    tracing::info!(addr = %LISTEN_ADDR, web_root = %web_root.display(), "control plane listening");

    axum::serve(listener, httpapi::router(&web_root))
        .with_graceful_shutdown(shutdown_signal())
        .await
        .context("serving HTTP")
}

/// Resolves on Ctrl-C or SIGTERM, so Kubernetes can stop the Pod cleanly.
async fn shutdown_signal() {
    let terminate = async {
        match tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate()) {
            Ok(mut signal) => {
                signal.recv().await;
            }
            Err(error) => {
                tracing::warn!(%error, "SIGTERM handler unavailable");
                std::future::pending::<()>().await;
            }
        }
    };
    tokio::select! {
        _ = tokio::signal::ctrl_c() => {}
        () = terminate => {}
    }
}
