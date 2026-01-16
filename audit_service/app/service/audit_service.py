import uuid
import httpx
import logging
from datetime import datetime
from app.domain.audit_event import AuditLogCreate, AuditLogResponse
from app.repository.audit_repository import AuditRepository
from app.settings import settings

logger = logging.getLogger(__name__)

class AuditService:
    """Core domain service - keeps business logic separate from framework"""

    def __init__(self, repository: AuditRepository, http_client: httpx.AsyncClient):
        self.repository = repository
        self.http_client = http_client

    async def log(self, audit_data: AuditLogCreate, request_id: str) -> AuditLogResponse:
        audit_id = str(uuid.uuid4())

        audit_record = {
            "id": audit_id,
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "service_name": audit_data.service_name,
            "action": audit_data.action,
            "entity_type": audit_data.entity_type,
            "entity_id": audit_data.entity_id,
            "performed_by": audit_data.performed_by,
            "performed_by_ip": audit_data.performed_by_ip,
            "client_id": audit_data.client_id,
            "context": audit_data.context,
            "old_value": audit_data.old_value,
            "new_value": audit_data.new_value,
            "success": audit_data.success,
            "error_message": audit_data.error_message,
        }

        # Main persistence
        await self.repository.save(audit_record)

        # Optional: async notification (webhook, event bus...)
        if settings.NOTIFY_WEBHOOK_URL:
            try:
                await self.http_client.post(
                    settings.NOTIFY_WEBHOOK_URL,
                    json={"event": "audit.created", "audit_id": audit_id},
                    timeout=3.0
                )
            except Exception as e:
                logger.warning(f"Webhook notification failed: {e}")

        return AuditLogResponse(
            id=audit_id,
            timestamp=datetime.fromisoformat(audit_record["timestamp"]),
            received_at=datetime.utcnow()
        )
