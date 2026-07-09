from datetime import datetime
from typing import Optional, Dict, Any

class Incident:
    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "",
        description: str = "",
        severity: str = "low",
        status: str = "open",
        channel_id: Optional[str] = None,
        message_ts: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.severity = severity
        self.status = status
        self.channel_id = channel_id
        self.message_ts = message_ts
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Incident":
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            severity=data.get("severity", "low"),
            status=data.get("status", "open"),
            channel_id=data.get("channel_id"),
            message_ts=data.get("message_ts"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "channel_id": self.channel_id,
            "message_ts": self.message_ts
        }
        if self.id is not None:
            res["id"] = self.id
        if self.created_at is not None:
            res["created_at"] = self.created_at
        if self.updated_at is not None:
            res["updated_at"] = self.updated_at
        return res
