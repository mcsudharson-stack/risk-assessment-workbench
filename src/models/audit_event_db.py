from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from src.config.database import Base


class AuditEventDB(Base):
    __tablename__ = "audit_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, nullable=False, index=True)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)

    from_status = Column(String, nullable=True)
    to_status = Column(String, nullable=True)

    details = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )