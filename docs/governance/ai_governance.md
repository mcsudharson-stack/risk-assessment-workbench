# AI Governance

## Purpose

The AI component assists FCRM analysts by preparing a draft financial crime risk assessment.

AI is a decision-support tool, not a decision maker.

## Human Control

The FCRM Analyst reviews the AI-generated assessment.

The analyst may:

- Agree with the AI assessment
- Change the risk rating
- Override the AI assessment

When an analyst overrides the AI output, an override reason must be recorded.

## Final Decision

The Risk Committee owns the final decision.

Possible outcomes are:

- Approved
- Rejected
- Changes Requested

The AI cannot approve or reject a change.

## Explainability

The system provides:

- Deterministic risk score
- Risk rating
- Reasons contributing to the score
- Retrieved policy sources
- AI-generated assessment
- Analyst comments
- Override reason
- Committee decision reason

## Auditability

Important workflow activities are recorded in the audit history.

This prototype provides an application-level append-only audit record.

## AI Safety

The AI prompt instructs the model to:

- Identify financial crime risks
- Explain why risks are relevant
- Identify supporting evidence
- Highlight missing information
- Avoid making final approval or rejection decisions

## Data Protection

The hackathon prototype uses synthetic data.

No real customer information or confidential banking data is required.

## AI Limitations

AI responses may contain incomplete or incorrect information.

Therefore:

1. AI output must be reviewed by an FCRM Analyst.
2. Human users remain accountable for decisions.
3. AI disagreement can be overridden.
4. Override reasoning is captured for governance and audit purposes.