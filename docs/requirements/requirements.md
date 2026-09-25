# Risk Assessment Workbench - Requirements

## Problem

Financial Crime Risk Management (FCRM) teams must assess risk whenever the bank introduces a new product, feature, process, vendor, geography, or customer segment.

The existing process relies heavily on email, Word, Excel, and SharePoint. This can take 15–20 business days and makes audit reconstruction difficult.

## Goal

Build an AI-assisted Risk Assessment Workbench that supports the complete workflow from change-request submission to Risk Committee decision.

## Users

- Product Owner
- FCRM Analyst
- Risk Committee

## Main Requirements

1. Product Owner can submit a change request.
2. System stores the request in a governed database.
3. System calculates a deterministic risk score.
4. System retrieves relevant policy information.
5. AI generates a draft FCRM risk assessment.
6. FCRM Analyst reviews the AI output.
7. Analyst can agree or override the AI assessment.
8. Override requires a reason.
9. Risk Committee makes the final decision.
10. System maintains an audit history.

## Possible Decisions

- Approved
- Rejected
- Changes Requested

## Important Constraint

AI must never automatically approve or reject a change.

Final decisions remain with human FCRM users.

## Data

This hackathon prototype uses synthetic data only.