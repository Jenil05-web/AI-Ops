from functools import partial
from langgraph.graph import StateGraph, END

from triage.agents.triage_agent import TicketState, triage_node
from triage.agents.retrieval_agent import retrieval_node
from triage.agents.drafting_agent import drafting_node
from triage.agents.escalation_agent import escalation_node
from triage.models.classifier import load_artifacts
from triage.rag.knowledge_base import build_knowledge_base

def build_graph(model_dir: str):
    """Build and compile the full ticket-processing graph."""
    model, vectorizer, label_encoder = load_artifacts(model_dir)
    index, df = build_knowledge_base()

    graph = StateGraph(TicketState)

    graph.add_node("triage", partial(triage_node, model=model, vectorizer=vectorizer, label_encoder=label_encoder))
    graph.add_node("retrieve", partial(retrieval_node, index=index, df=df))
    graph.add_node("draft", drafting_node)
    graph.add_node("escalate", escalation_node)

    graph.set_entry_point("triage")
    graph.add_edge("triage", "retrieve")
    graph.add_edge("retrieve", "draft")
    graph.add_edge("draft", "escalate")
    graph.add_edge("escalate", END)

    return graph.compile()

# Note functools.partial — this is how we "pre-bind" the extra arguments (model, vectorizer, etc.) to each node function,since LangGraph expects every node to accept just (state).
# This is a clean way to inject dependencies without using global variables.