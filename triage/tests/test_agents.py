from unittest.mock import MagicMock
from triage.agents.triage_agent import triage_node
from triage.agents.escalation_agent import escalation_node
from triage.agents.drafting_agent import build_draft_prompt


def test_triage_node_sets_predicted_queue():
    fake_model = MagicMock()
    fake_vectorizer = MagicMock()
    fake_label_encoder = MagicMock()

    fake_vectorizer.transform.return_value = "fake_vector"
    import numpy as np
    fake_model.predict_proba.return_value = np.array([[0.9, 0.1]])
    fake_label_encoder.inverse_transform.return_value = ["Technical Support"]

    state = {"ticket_text": "internet keeps dropping"}
    result = triage_node(state, fake_model, fake_vectorizer, fake_label_encoder)

    assert result['predicted_queue'] == "Technical Support"


def test_escalation_node_flags_high_risk_queue():
    state = {"predicted_queue": "Billing and Payments"}
    result = escalation_node(state)
    assert result['escalated'] is True


def test_escalation_node_does_not_flag_normal_queue():
    state = {"predicted_queue": "Technical Support"}
    result = escalation_node(state)
    assert result['escalated'] is False


def test_build_draft_prompt_includes_ticket_and_context():
    context = [{"body": "old problem", "answer": "old fix"}]
    prompt = build_draft_prompt("new problem", context)
    assert "new problem" in prompt
    assert "old fix" in prompt

"""Note MagicMock — new concept here: instead of monkeypatch swapping one function (what we did for RAG), 
 MagicMock creates a fake object that pretends to be your model/vectorizer/encoder, letting you control exactly what .predict() or .transform() returns without needing the real trained artifacts. 
Same goal as monkeypatch (avoid real dependencies in tests), different tool for a different shape of problem (mocking objects vs. mocking functions)."""