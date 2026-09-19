from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Severity(str, Enum): LOW='LOW'; MEDIUM='MEDIUM'; HIGH='HIGH'; CRITICAL='CRITICAL'
class EventIn(BaseModel):
    event_id: str = Field(min_length=8, max_length=80)
    timestamp: datetime
    source_ip: str = Field(min_length=3, max_length=64)
    source_port: int = Field(ge=1, le=65535)
    destination_port: int = Field(ge=1, le=65535)
    protocol: str = Field(min_length=1, max_length=20)
    service: str = Field(min_length=1, max_length=40)
    event_type: str = Field(min_length=1, max_length=60)
    demo: bool = False
class EventOut(EventIn):
    model_config = ConfigDict(from_attributes=True)
    id: int; risk_score: int; severity: Severity; threat_category: Optional[str] = None
class AlertOut(BaseModel):
    id: int; event_id: str; severity: Severity; message: str; status: str; created_at: datetime
