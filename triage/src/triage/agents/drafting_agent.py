import os
from openai import OpenAI
from triage.agents.triage_agent import TicketState

llm_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def build_draft_prompt(ticket_text: str, retrieved_context: list) -> str:
    context_str = "\n\n".join(
        f"{i+1}. {r['answer']}" for i, r in enumerate(retrieved_context)
    )
    return f"""You are a technical support specialist. Your job is to resolve customer issues directly using only proven prior resolutions.

CUSTOMER ISSUE:
"{ticket_text}"

PROVEN RESOLUTIONS FROM SIMILAR PAST TICKETS:
{context_str}

INSTRUCTIONS:
- Identify which proven resolution(s) above are most relevant to the customer's specific issue.
- Write a direct answer that resolves the issue using that information. Do not invent steps that are not supported by the resolutions above.
- Do not write a greeting, subject line, sign-off, or any email formatting. Output only the resolution content itself.
- Do not ask the customer for more information unless none of the resolutions above provide any usable answer.
- Keep the response under 80 words.
- Address the customer's exact issue — do not include general advice unrelated to their specific problem.

RESPONSE:"""


def drafting_node(state: TicketState, model: str = "gpt-4o-mini") -> TicketState:
    """Generate a grounded draft response using retrieved context."""
    prompt = build_draft_prompt(state['ticket_text'], state['retrieved_context'])
    response = llm_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    state['draft_response'] = response.choices[0].message.content
    return state

