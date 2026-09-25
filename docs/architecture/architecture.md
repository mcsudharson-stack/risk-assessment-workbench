# Risk Assessment Workbench - Architecture

## High-Level Architecture

Product Owner
      |
      v
Streamlit UI
      |
      v
FastAPI Backend
      |
      +----------------------+
      |                      |
      v                      v
SQLite Database        Risk Assessment Workflow
                             |
                             v
                    Deterministic Risk Scoring
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
                       Human Review
                             |
                             v
                      Risk Committee
                             |
                             v
                      Final Decision

## Main Components

### Frontend

Streamlit provides the user interface for:

- Dashboard
- Change request submission
- AI risk assessment
- Analyst review
- Committee decision
- Audit history

### Backend

FastAPI provides REST APIs for the application workflow.

### Database

SQLite stores:

- Change requests
- Workflow status
- Analyst reviews
- Committee decisions
- Audit events

### Risk Engine

The risk engine calculates a deterministic score using:

- Change type
- Geography
- Customer segment
- Vendor involvement

### AI Layer

The AI layer uses:

- Groq LLM
- Prompt engineering
- Local policy retrieval
- Risk assessment generation

AI output is advisory only.

### Human-in-the-Loop

The workflow contains two important human controls:

FCRM Analyst Review
        |
        v
Risk Committee Decision

AI cannot make the final business decision.

## Deployment

The application is containerized using Docker.

Two containers are used:

- FastAPI backend
- Streamlit frontend

GitHub Actions automatically runs project tests when code is pushed.