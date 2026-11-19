use async_trait::async_trait;
use axum::extract::*;
use axum_extra::extract::CookieJar;
use bytes::Bytes;
use headers::Host;
use http::Method;
use serde::{Deserialize, Serialize};

use crate::{models, types::*};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[must_use]
#[allow(clippy::large_enum_variant)]
pub enum GetHealthzResponse {
    /// The control plane is serving requests.
    Status200_TheControlPlaneIsServingRequests
    (models::Health)
}




/// Health
#[async_trait]
#[allow(clippy::ptr_arg)]
pub trait Health<E: std::fmt::Debug + Send + Sync + 'static = ()>: super::ErrorHandler<E> {
    /// Report that the control plane is serving requests.
    ///
    /// GetHealthz - GET /api/v1/healthz
    async fn get_healthz(
    &self,
    
    method: &Method,
    host: &Host,
    cookies: &CookieJar,
    ) -> Result<GetHealthzResponse, E>;
}
