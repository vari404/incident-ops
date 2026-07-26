from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=2000)
    customer_email: str = Field(min_length=5, max_length=255)
    priority: TicketPriority = TicketPriority.MEDIUM


class Ticket(TicketCreate):
    id: int
    status: TicketStatus
    assigned_agent: str | None = None
    created_at: datetime
    updated_at: datetime