from pydantic import BaseModel, Field


class AnalystReview(BaseModel):
    analyst_name: str = Field(
        ...,
        description="Name or ID of the FCRM analyst",
    )

    final_risk_rating: str = Field(
        ...,
        description="Analyst final risk rating: LOW, MEDIUM, or HIGH",
    )

    override_ai: bool = Field(
        False,
        description="Whether the analyst disagrees with the AI assessment",
    )

    override_reason: str | None = Field(
        None,
        description="Required when the analyst overrides the AI assessment",
    )

    comments: str | None = Field(
        None,
        description="Additional analyst comments",
    )