from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

from app.settings import settings
from app.api.audit_controller import router as audit_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = httpx.AsyncClient(
        timeout=5.0,
        limits=httpx.Limits(max_connections=50, max_keepalive_connections=10)
    )
    app.state.http_client = client
    # In a real app, initialize DB connections here
    print(f"{settings.APP_NAME} started")
    
    yield
    
    # Shutdown
    await client.aclose()
    print(f"{settings.APP_NAME} shutdown")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None
)

app.include_router(audit_router, prefix="/v1", tags=["audit"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "audit-service"}
