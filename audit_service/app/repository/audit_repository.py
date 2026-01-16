from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AuditRepository(ABC):
    @abstractmethod
    async def save(self, audit_record: Dict[str, Any]) -> None:
        pass

class InMemoryAuditRepository(AuditRepository):
    def __init__(self):
        self.storage: List[Dict[str, Any]] = []
        
    async def save(self, audit_record: Dict[str, Any]) -> None:
        self.storage.append(audit_record)
        # For demo purposes
        # print(f"DEBUG: Stored audit record {audit_record['id']}")
