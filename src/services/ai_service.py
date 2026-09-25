from pathlib import Path

from groq import Groq

from src.config.settings import settings
from src.services.knowledge_service import retrieve_policy_context


client = Groq(api_key=settings.groq_api_key)


def generate_risk_assessment(change_request, risk_result):
    # Read the AI system prompt
    prompt_path = Path("ai/prompts/risk_assessment_prompt.txt")
    system_prompt = prompt_path.read_text(encoding="utf-8")

    # Retrieve relevant policy documents
    policy_documents = retrieve_policy_context(change_request)

    # Convert retrieved documents into text for the LLM
    policy_context = "\n\n".join(
        f"SOURCE: {document['source']}\n{document['content']}"
        for document in policy_documents
    )

    # Build the user prompt
    user_prompt = f"""
CHANGE REQUEST

Name: {change_request.name}
Description: {change_request.description}
Change Type: {change_request.change_type}
Business Unit: {change_request.business_unit}
Geography: {change_request.geography}
Customer Segment: {change_request.customer_segment}
Vendor Involved: {change_request.vendor_involved}

DETERMINISTIC RISK RESULT

Risk Score: {risk_result["score"]}
Risk Rating: {risk_result["rating"]}
Risk Reasons: {risk_result["reasons"]}

POLICY CONTEXT

{policy_context}

INSTRUCTIONS

Use the policy context above as evidence.

Clearly identify any missing information.

Do not approve or reject the change.

The final decision must remain with the human FCRM Analyst and Risk Committee.

Prepare the draft FCRM risk assessment.
"""

    # Send the grounded prompt to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content