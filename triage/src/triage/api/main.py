from fastapi import FastAPI
from triage.agents.graph import build_graph
from triage.api import routes

app = FastAPI(title="Triage API", version="0.1.0")
app.include_router(routes.router)


@app.on_event("startup")
def load_graph():
    graph = build_graph(model_dir="models")
    routes.set_graph(graph)