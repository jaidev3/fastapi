from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from dataclasses import dataclass

class AuditAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXECUTE = "EXECUTE"
    VIEW = "VIEW"
    OTHER = "OTHER"


class AuditLogCreate(BaseModel):
    """Input model for audit logging (what services should send)"""
    service_name: str = Field(..., min_length=3, max_length=50)
    action: AuditAction
    entity_type: str = Field(..., min_length=1, max_length=50)
    entity_id: Optional[str] = None
    performed_by: str = Field(..., description="user id / service account / system")
    performed_by_ip: Optional[str] = None
    client_id: Optional[str] = None  # e.g. frontend app / mobile
    context: Dict[str, Any] = Field(default_factory=dict, description="additional context")
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    success: bool = True
    error_message: Optional[str] = None


@dataclass(frozen=True)
class AuditLogResponse:
    id: str
    timestamp: datetime
    received_at: datetime
