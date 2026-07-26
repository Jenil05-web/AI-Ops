from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from triage.api.main import app
from triage.api import routes


def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_ticket_returns_expected_shape():
    fake_graph = MagicMock()
    fake_graph.invoke.return_value = {
        "ticket_text": "test issue",
        "predicted_queue": "Technical Support",
        "retrieved_context": [
            {"subject": "s", "body": "b", "answer": "a", "distance": 0.5}
        ],
        "draft_response": "Here is a fix.",
        "escalated": False,
    }
    routes.set_graph(fake_graph)

    client = TestClient(app)
    response = client.post("/process-ticket", json={"ticket_text": "test issue"})

    assert response.status_code == 200
    body = response.json()
    assert body["predicted_queue"] == "Technical Support"
    assert body["escalated"] is False