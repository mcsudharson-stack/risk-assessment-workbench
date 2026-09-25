# Risk Assessment Workbench

AI-assisted Financial Crime Risk Management (FCRM) workbench for assessing risks introduced by new products, features, processes, vendors, geographies, and customer segments.

## Problem

Financial institutions must assess financial-crime risk before significant business changes go live.

Traditional assessments may depend on email, Word, Excel, and SharePoint, which can result in:

- Long assessment cycles
- Inconsistent analyst outcomes
- Manual record keeping
- Difficult audit reconstruction

## Solution

The Risk Assessment Workbench provides a governed workflow:

Change Request
→ Risk Scoring
→ Policy Retrieval
→ AI Draft Assessment
→ FCRM Analyst Review
→ Risk Committee Decision
→ Audit History

AI assists human reviewers but does not make final approval or rejection decisions.

## Users

### Product Owner

Submits a new business change for assessment.

### FCRM Analyst

Reviews:

- Risk score
- Risk factors
- Policy evidence
- AI-generated assessment

The analyst can override the AI assessment, but an override reason must be recorded.

### Risk Committee

Makes the final decision:

- Approved
- Rejected
- Changes Requested

## Key Features

- Change request management
- Deterministic risk scoring
- Policy knowledge retrieval
- Groq LLM integration
- AI-generated FCRM assessment
- Human-in-the-loop review
- AI override tracking
- Risk Committee decision workflow
- Audit history
- Streamlit dashboard
- FastAPI REST APIs
- Automated tests
- Docker containerization
- GitHub Actions CI

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### AI

- Groq
- LLM prompting
- Local policy retrieval
- AI-assisted risk assessment

### Frontend

- Streamlit
- Plotly

### Testing

- Pytest

### DevOps

- Git
- GitHub
- GitHub Actions
- Docker
- Docker Compose

## Architecture

```text
Product Owner
      |
      v
Streamlit UI
      |
      v
FastAPI Backend
      |
      +-------------------+
      |                   |
      v                   v
SQLite DB          Risk Assessment Workflow
                          |
                          v
                 Deterministic Scoring
                          |
                          v
                   Policy Retrieval
                          |
                          v
                      Groq LLM
                          |
                          v
                  AI Draft Assessment
                          |
                          v
                   FCRM Analyst
                          |
                          v
                   Risk Committee
                          |
                          v
                   Final Decision