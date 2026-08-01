from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from triage.agents.graph import build_graph
from triage.api import routes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Triage API", version="0.1.0")
app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://ai-ops-triage.onrender.com",
        "*"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
app.include_router(routes.router)


@app.on_event("startup")
def load_graph():
    from triage.db.database import init_db
    init_db()
    
    graph = build_graph(model_dir="models")
    routes.set_graph(graph)

# This file is basically about loading the graph and setting it in the routes so that it can be used in the API endpoints.
#  The graph is built using the build_graph function from triage.agents.graph module, which loads the model artifacts and prepares the inference pipeline.
#  The graph is then set in the routes module using the set_graph function, allowing the API endpoints to access it for processing tickets and making predictions.
