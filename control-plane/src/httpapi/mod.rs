//! HTTP entrypoint: mounts the generated API routes and serves the web app from the same origin.

use std::{path::Path, sync::Arc};

use armoury_httpapi::{
    apis::{
        ErrorHandler,
        health::{GetHealthzResponse, Health},
    },
    models,
};
use async_trait::async_trait;
use axum::{Router, routing::any};
use axum_extra::extract::CookieJar;
use headers::Host;
use http::{Method, StatusCode};
use tower_http::services::{ServeDir, ServeFile};

/// Implements the API traits generated from `api/openapi.yaml`.
#[derive(Clone, Copy, Debug, Default)]
pub struct Api;

impl ErrorHandler for Api {}

#[async_trait]
impl Health for Api {
    async fn get_healthz(
        &self,
        _method: &Method,
        _host: &Host,
        _cookies: &CookieJar,
    ) -> Result<GetHealthzResponse, ()> {
        Ok(
            GetHealthzResponse::Status200_TheControlPlaneIsServingRequests(models::Health::new(
                "ok".to_owned(),
            )),
        )
    }
}

/// The API under `/api`, and the web app (with `index.html` as the SPA fallback) everywhere else.
pub fn router(web_root: &Path) -> Router {
    let web_app = ServeDir::new(web_root).fallback(ServeFile::new(web_root.join("index.html")));
    armoury_httpapi::server::new(Arc::new(Api))
        .route("/api/{*rest}", any(|| async { StatusCode::NOT_FOUND }))
        .fallback_service(web_app)
}

#[cfg(test)]
mod tests {
    use axum::body::{Body, to_bytes};
    use http::{Request, header::HOST};
    use tower::ServiceExt;

    use super::*;

    /// Serves `uri` from a router whose web root holds only an `index.html`, then removes it.
    async fn get(test: &str, uri: &str) -> (StatusCode, String) {
        let root =
            std::env::temp_dir().join(format!("armoury-httpapi-{test}-{}", std::process::id()));
        std::fs::create_dir_all(&root).unwrap();
        std::fs::write(root.join("index.html"), "<title>Armoury</title>").unwrap();

        let request = Request::get(uri)
            .header(HOST, "localhost")
            .body(Body::empty())
            .unwrap();
        let response = router(&root).oneshot(request).await.unwrap();
        let status = response.status();
        let body = to_bytes(response.into_body(), 1 << 20).await.unwrap();
        std::fs::remove_dir_all(&root).unwrap();
        (status, String::from_utf8(body.to_vec()).unwrap())
    }

    #[tokio::test]
    async fn healthz_reports_ok() {
        let (status, body) = get("healthz", "/api/v1/healthz").await;
        assert_eq!(
            (status, body.as_str()),
            (StatusCode::OK, r#"{"status":"ok"}"#)
        );
    }

    #[tokio::test]
    async fn client_routes_fall_back_to_the_web_app() {
        let (status, body) = get("spa", "/issues").await;
        assert_eq!(
            (status, body.as_str()),
            (StatusCode::OK, "<title>Armoury</title>")
        );
    }

    #[tokio::test]
    async fn unknown_api_routes_are_not_found() {
        let (status, _) = get("unknown-api", "/api/v1/nothing-here").await;
        assert_eq!(status, StatusCode::NOT_FOUND);
    }
}
