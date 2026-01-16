import uuid
from fastapi import APIRouter, HTTPException, Request, Depends, status
from app.domain.audit_event import AuditLogCreate, AuditLogResponse
from app.service.audit_service import AuditService
from app.repository.audit_repository import AuditRepository, InMemoryAuditRepository

router = APIRouter()

# Simple singleton for in-memory repo so data persists across requests
_repo_instance = InMemoryAuditRepository()

def get_repository() -> AuditRepository:
    return _repo_instance

async def get_audit_service(request: Request, repo: AuditRepository = Depends(get_repository)) -> AuditService:
    if not hasattr(request.app.state, "http_client"):
        raise HTTPException(status_code=500, detail="HTTP Client not initialized")
    return AuditService(
        repository=repo,
        http_client=request.app.state.http_client
    )

@router.post(
    "/audit",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create audit log entry",
    description="Used by other services to record important actions"
)
async def create_audit_log(
    audit_data: AuditLogCreate,
    request: Request,
    audit_service: AuditService = Depends(get_audit_service)
):
    """
    Main endpoint for audit logging
    """
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    try:
        result = await audit_service.log(audit_data, request_id)
        return result

    except Exception as e:
        # Log the error (in a real app, use the structured logger)
        print(f"Error storing audit log: {e}")
        raise HTTPException(
            status_code=500,
            detail="Audit logging failed. Please try again later."
        )
