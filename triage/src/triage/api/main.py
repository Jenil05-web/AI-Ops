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
    allow_origins=["*"],   # fine for local dev; restrict in real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.on_event("startup")
def load_graph():
    graph = build_graph(model_dir="models")
    routes.set_graph(graph)