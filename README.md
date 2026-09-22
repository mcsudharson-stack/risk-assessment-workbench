# Risk Assessment Workbench

AI-assisted financial crime risk assessment platform for assessing
financial crime risk introduced by new products, features, process
changes, vendors, geographies, and customer segments.

## Problem

The current risk assessment process relies heavily on email,
documents, spreadsheets, and manual analysis.

This project aims to provide a governed workflow that moves a
change request from intake through assessment and committee
decision while maintaining human oversight and auditability.

## Goals

- Reduce assessment preparation time
- Standardize risk assessment
- Provide traceability for risk ratings
- Retrieve relevant policies and guidance
- Support analysts with AI-generated assessment drafts
- Maintain human decision-making
- Maintain an immutable audit trail
- Support configurable scoring and workflow rules

## Technology

- Python
- FastAPI
- LangGraph
- LangChain
- PostgreSQL
- pgvector
- Streamlit
- Docker
- pytest

## Project Structure

```text
src/          Application backend
ai/           AI prompts, agents and guidance
data/         Synthetic data and knowledge base
docs/         Requirements, architecture and governance
evals/        AI evaluation datasets and results
tests/        Automated tests
ops/          Deployment and operations
frontend/     User interface