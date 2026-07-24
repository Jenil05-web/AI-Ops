from triage.agents.triage_agent import TicketState
from triage.rag.retriever import search

def retrieval_node(state: TicketState, index, df, k: int = 3) -> TicketState:
    """Retrieve top-k similar past tickets and their resolutions."""
    results = search(state['ticket_text'], index, df, k=k)
    state['retrieved_context'] = results.to_dict('records')
    return state