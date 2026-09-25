from enum import Enum

from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    NEW_PRODUCT = "new_product"
    NEW_FEATURE = "new_feature"
    PROCESS_CHANGE = "process_change"
    NEW_VENDOR = "new_vendor"
    NEW_GEOGRAPHY = "new_geography"
    NEW_CUSTOMER_SEGMENT = "new_customer_segment"


class ChangeRequestStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    COMMITTEE_REVIEW = "committee_review"
    DECIDED = "decided"


class ChangeRequest(BaseModel):
    request_id: str = Field(..., description="Unique change request ID")
    name: str = Field(..., description="Name of the proposed change")
    description: str = Field(..., description="Description of the proposed change")

    change_type: ChangeType

    business_unit: str
    geography: str
    customer_segment: str

    vendor_involved: bool = False

    submitted_by: str

    status: ChangeRequestStatus = ChangeRequestStatus.SUBMITTED