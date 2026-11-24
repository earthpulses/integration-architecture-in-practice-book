"""Typed validation and mapping for an order, with a governed code list."""
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

STATUS_MAP = {"1": "New", "2": "Accepted", "3": "Shipped", "9": "Cancelled"}

class OrderIn(BaseModel):
    id: str                                     # IDs are strings: keep zeros
    total: Decimal = Field(ge=0)                # never float for money
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    status: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def must_have_zone(cls, v):
        if v.tzinfo is None:
            raise ValueError("timestamp must include a time zone")
        return v.astimezone(timezone.utc)

def to_target(o):
    if o.status not in STATUS_MAP:
        raise ValueError("unmapped status %r" % o.status)   # quarantine
    return {"externalId": o.id, "amount": str(o.total), "currency": o.currency,
            "status": STATUS_MAP[o.status], "createdAt": o.created_at.isoformat()}
