# AI-Ops — Full Project Summary

## Phase 1: The Pipeline

**Data**
Sourced and validated ticket data — discovered a first dataset's labels had no real relationship to the text (caught by manually reading samples, not just trusting stats), rejected it, and moved to a second dataset with genuine signal. Cleaned it into a usable classifier/RAG-ready format.

**Classical ML**
Built a ticket-routing classifier: TF-IDF + Logistic Regression baseline (46% accuracy) → improved with XGBoost (50% accuracy, better minority-class performance) — predicting which support queue a ticket belongs to.

**RAG**
Built a retrieval layer using OpenAI embeddings + FAISS over real historical ticket resolutions, validated with RAGAS (context precision, faithfulness, answer relevancy) — diagnosed and fixed a prompt-quality issue using those metrics rather than guessing.

**Agents**
Orchestrated the classifier, retriever, an LLM drafting step (GPT-4o-mini), and rule-based escalation logic into one LangGraph pipeline — using each technique only where it was actually the right tool, not by default.

**Engineering**
Converted every notebook into a real installable Python package (`src/` layout, `pip install -e .`), with config management, structured logging, and unit tests (with proper mocking) across every layer. Wrapped it in a FastAPI service, containerized with Docker, wrote (but did not fully verify) CI.

**Frontend v1**
Built a "pipeline inspector" UI — a rail animation showing each agent stage lighting up as a ticket was processed.

## Phase 2: From Pipeline to Product

Realized after finishing Phase 1 that a fully working, well-engineered pipeline still _felt_ like a chatbot — because every ticket, regardless of quality, ended up displayed as a single text-in/text-out exchange with no persistence, memory, or real product behavior.

**Fixes:**

- Added a **persistence layer** (SQLite + SQLAlchemy) — tickets became stateful records with an ID and lifecycle, not one-shot API calls
- Exposed **classifier confidence** as a real signal (`predict_proba`) instead of discarding it after choosing the top label
- Built a **decision layer** (`decide_status()`) that combines confidence + retrieval distance + queue risk to classify every ticket as `auto_resolved`, `needs_review`, or `escalated` — with hard rules ensuring high-risk topics (billing, HR, outages) always get human review
- Extended the API with stateful endpoints (`/tickets`, `/stats`, `/tickets/{id}/reply`) and a live **automation-rate metric**, turning "this reduces human workload" into a real, computed number instead of a claim
- Debugged real integration bugs using actual tracebacks (a stale file, a broken state field) rather than guesswork
- Reframed the frontend from a single pipeline-visualization screen into two purpose-built interfaces: a **customer portal** (submit/check a request) and an **agent console** (a real inbox showing only what needs a human, plus a read-only auto-resolved audit log) — with the original pipeline inspector kept as an internal dev/demo tool

## What this project actually demonstrates

A mixed-technique system (classical ML + retrieval + LLM + rule-based logic) used deliberately rather than defaulting to "just prompt an LLM for everything" — with real production practices (testing, packaging, config, containerization, persistence) and a documented decision-making trail showing _why_ the architecture evolved, not just what was built.
