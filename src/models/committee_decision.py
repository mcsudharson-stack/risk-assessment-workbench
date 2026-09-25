from typing import Literal

from pydantic import BaseModel, Field


class CommitteeDecision(BaseModel):
    committee_member: str = Field(
        ...,
        description="Name or ID of the Risk Committee member",
    )

    decision: Literal[
        "approved",
        "rejected",
        "changes_requested",
    ]

    reason: str = Field(
        ...,
        min_length=5,
        description="Reason for the committee decision",
    )