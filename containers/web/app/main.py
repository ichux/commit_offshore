from fastapi import FastAPI

from .api.v1 import additional_endpoints, endpoints

app = FastAPI(title="User Management API")

app.include_router(endpoints.router, prefix="/v1", tags=["Basic Endpoints"])
app.include_router(
    additional_endpoints.router, prefix="/v1", tags=["Additional Endpoints"]
)
