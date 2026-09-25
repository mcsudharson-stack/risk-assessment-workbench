# Supervisory Framework Alignment

## Purpose

The Risk Assessment Workbench is a hackathon prototype.

Its risk-assessment approach is informed by publicly available banking supervisory guidance. The prototype does not claim to reproduce a bank's internal regulatory methodology or replace compliance judgement.

## 1. FFIEC BSA/AML Risk Assessment

The FFIEC BSA/AML Examination Manual describes a risk-based approach to identifying and assessing money laundering, terrorist financing, and other illicit-finance risks.

Relevant risk categories include:

- Products and services
- Customers
- Geographic locations

Our workbench reflects these concepts by collecting information about:

- Change type
- Customer segment
- Geography
- Business activity
- Vendor involvement

The system then provides a documented risk assessment for human review.

## 2. OFAC Sanctions Compliance

The U.S. Treasury Office of Foreign Assets Control (OFAC) publishes a Framework for OFAC Compliance Commitments.

Our AI assessment includes sanctions risk as one of the areas that must be considered.

The AI can identify potential sanctions-related concerns, but it cannot make the final compliance decision.

## 3. Third-Party Risk Management

Federal banking agencies provide interagency guidance for managing risks arising from third-party relationships.

Our workbench therefore captures whether a proposed change involves an external vendor.

Vendor involvement contributes to the prototype risk assessment and can trigger additional analyst review.

## 4. Customer Risk

The FFIEC BSA/AML guidance emphasizes a risk-based approach to customer due diligence.

Our workbench captures the customer segment associated with a proposed change and uses that information as one input to the assessment.

No customer category is automatically treated as determinative of the final financial-crime risk.

## 5. Human Judgement

Risk factors are not treated as automatic approval or rejection rules.

The deterministic score and AI-generated assessment provide decision support.

The FCRM Analyst reviews the assessment and may disagree with the AI.

The Risk Committee remains responsible for the final decision.

## Prototype Limitation

The scoring weights used in this hackathon are synthetic demonstration values.

They are not regulatory thresholds and should not be interpreted as official FFIEC, OFAC, Federal Reserve, FDIC, OCC, or FinCEN scoring rules.