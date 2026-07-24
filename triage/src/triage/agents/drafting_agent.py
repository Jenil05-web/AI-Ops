import os
from openai import OpenAI
from triage.agents.triage_agent import TicketState

llm_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def build_draft_prompt(ticket_text:str, retrieved_context:list )-> str:
    context_str = "\n\n".join(
        f"Past ticket: {r['body']}\nResolution given: {r['answer']}"
        for r in retrieved_context
    )
    return f"""You are a customer support agent. A customer submitted this ticket:
    "{ticket_text}"
    Here are similar past tickets and how they were resolved:
    {context_str}
Using this context, draft a helpful, concise response to the customer. Do not mention that you referenced past tickets."""


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


