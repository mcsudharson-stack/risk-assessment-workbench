from sqlalchemy import Boolean, Column, String, Text

from src.config.database import Base


class ChangeRequestDB(Base):
    __tablename__ = "change_requests"

    request_id = Column(String, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    change_type = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)
    geography = Column(String, nullable=False)
    customer_segment = Column(String, nullable=False)

    vendor_involved = Column(Boolean, default=False)

    submitted_by = Column(String, nullable=False)

    status = Column(
        String,
        nullable=False,
        default="submitted",
    )

    decision = Column(
        String,
        nullable=True,
    )

    analyst_name = Column(
        String,
        nullable=True,
    )

    analyst_risk_rating = Column(
        String,
        nullable=True,
    )

    ai_overridden = Column(
        Boolean,
        nullable=True,
    )

    override_reason = Column(
        Text,
        nullable=True,
    )

    analyst_comments = Column(
        Text,
        nullable=True,
    )