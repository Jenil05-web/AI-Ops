# Quick summary so far

Week 1 (Day 1-3)

Explored & validated 2 datasets, ditched first (fake labels), committed to real ticketing dataset
Cleaned data → cleaning.py (filter, dedupe, strip HTML, build text_input)
Trained classifier (TF-IDF + XGBoost, 50% acc) → classifier.py + train.py
Installed project as a real package (pyproject.toml, pip install -e .)
Rewrote notebooks to call the package instead of holding raw logic
Wrote & passed tests/test_data.py
Wrote & passed test_classifer.py file

# Week 1 — Complete Summary -- completed

Data : ( Basically model ne load karvu pachi ema apada needs na according changes karva etc... ( to make the data relevant to use))

Explored first dataset (synthetic support tickets) — discovered labels had no real relationship to ticket text, killed the plan (both classifier target and RAG source)
Sourced and validated a second dataset (real multilingual support tickets with real agent responses) — confirmed via manual read-through that labels genuinely match content
Cleaned to 22,053 English tickets: dropped PII/sparse columns, deduped, stripped HTML artifacts, engineered text_input

Modeling : ( Model ne train karvu (logistic regression) jenathi e tickets upar thi learn kari new response predict kari sake XGBoost uesd to increase the performace)

Baseline: TF-IDF + Logistic Regression → 46% accuracy (target: queue, 10 classes)
Improved: TF-IDF + XGBoost → 50% accuracy, better minority-class performance
Identified class imbalance as the main limitation (documented as future improvement, not fixed now — correct MVP call)

Engineering / Production ( Testing each and every function extracting notebook logic to production code)

Extracted notebook logic into a real package: src/triage/data/cleaning.py, src/triage/models/classifier.py, src/triage/models/train.py
Made the project pip-installable (pyproject.toml, pip install -e .)
Rewrote notebooks to import from the package instead of holding raw logic — notebooks are now thin demos, .py files hold the real logic
Wrote and passed unit tests for both cleaning (test_data.py) and classifier (test_classifier.py)

# Week 2 - Complete Summary :

Built RAG layer — OpenAI embeddings on 22k tickets → FAISS index → retriever returns relevant past tickets + real agent answers for a new query → packaged, tested.

Built 4-node agent pipeline: Triage (your XGBoost classifier) → Retrieval (FAISS + OpenAI embeddings) → Drafting (GPT-4o-mini, grounded in retrieved context) → Escalation (rule-based, flags high-risk queues)

Wired it into a real LangGraph graph (build_graph()), tested end-to-end — full pipeline runs from raw ticket text to a grounded draft response + escalation flag

Extracted all logic into .py modules (agents/triage_agent.py, retrieval_agent.py, drafting_agent.py, escalation_agent.py, graph.py), using functools.partial to inject dependencies cleanly (no globals)

Wrote and passed tests/test_agents.py using MagicMock (new technique — mocking objects, not just functions)

Built a 20-sample eval set combining classifier + RAG + drafting outputs

Used RAGAS to score retrieval/generation: context_precision (retrieval quality), faithfulness (grounding), answer_relevancy (question-answer match)

Diagnosed weak initial scores as a prompt engineering issue, not a retrieval issue (context_precision was already 1.0)

Iterated on the drafting prompt — improved faithfulness and relevancy after fixing formatting/verbosity issues and confirming kernel reload

Documented final scores as the project's baseline evaluation numbers (put actual final numbers here in your notebook)

# Week 4 — From Pipeline to Product

Context: After finishing the core pipeline (classifier → RAG → agents → API → Docker → frontend), I realized the project still felt like a chatbot — type text in, get text back — even though real ML/RAG/agent engineering was happening underneath. The issue wasn't the engineering, it was that nothing in the product surfaced the fact that the system was making real decisions. This week was about fixing that.

1. Added persistence (SQLite + SQLAlchemy)

The pipeline was stateless — every request vanished after returning a response. I built a real data layer:

models.py — a Ticket table (ID, customer info, pipeline outputs, status, timestamps)
database.py — SQLite engine/session setup, including the check_same_thread=False fix required for FastAPI's multi-threaded request handling
crud.py — create/update/fetch/list functions, plus a get_today_stats() query for automation metrics

This gave tickets an actual lifecycle instead of being one-shot request/response calls.

2. Exposed classifier confidence, not just the predicted label

Updated classifier.py's predict() to return (label, confidence) using predict_proba(), and propagated that change through the agent state and every downstream caller. This surfaced a signal that already existed inside the model but was previously being thrown away.

3. Built real decision logic (decision.py)

Wrote decide_status() — a function that uses predicted queue, classifier confidence, and RAG retrieval distance to route each ticket into one of three outcomes: auto_resolved, needs_review, or escalated. High-risk queues (billing, HR, outages) are never auto-sent regardless of confidence; low confidence with a weak retrieval match escalates immediately; strong confidence with a close match auto-resolves. This is the core fix — the system now decides for itself instead of routing every single ticket to a human by default.

4. Wired everything into real API endpoints

Added POST /tickets (submit → run pipeline → decide outcome → persist), GET /tickets (filterable by status), GET /tickets/{id}, POST /tickets/{id}/reply, and GET /stats — turning the system from "an endpoint that runs a pipeline" into "a system with a real inbox and an audit trail."

5. Debugged two real production bugs
   A stale routes.py file caused a false Method Not Allowed — traced back to an edit that never got saved before restarting the server.
   A KeyError: 'confidence' 500 error, traced through the actual traceback to a missing state field in triage_node that hadn't been updated during the confidence refactor.

Both were resolved by reading real tracebacks rather than guessing — same debugging discipline used earlier when diagnosing the bad first dataset.
Eighty percent institution mechanical it is your turn even the basket equal to water for you when it's your turn
6. Validated the decision logic against real requests

Ran multiple test tickets (billing, password reset, router issues) through the live API and confirmed: high-risk queues always route to review regardless of confidence, low-confidence tickets get flagged appropriately, and auto-resolution is genuinely reachable — checked against the classifier's actual confidence distribution rather than an arbitrary threshold.

Phase 2 — Changes Made
Added a persistence layer — introduced SQLite with SQLAlchemy (models.py, database.py, crud.py) to give tickets a real identity and lifecycle, replacing the previous stateless request/response pattern.
Exposed classifier confidence as a usable signal — modified classifier.py's predict() to return (label, confidence) via predict_proba() instead of only the predicted label, and propagated this change through the agent state and all downstream callers.
Built a rule-based decision layer — created decision.py with a decide_status() function that combines predicted queue, classifier confidence, and RAG retrieval distance to classify every ticket into one of three outcomes: auto_resolved, needs_review, or escalated.
Enforced a safety rule for high-risk categories — tickets in sensitive queues (Billing, HR, Service Outages) are never auto-sent regardless of confidence, ensuring the highest-stakes topics always get human review.
Extended the API with stateful endpoints — added POST /tickets (submit → run pipeline → decide outcome → persist), GET /tickets (filterable by status), GET /tickets/{id}, POST /tickets/{id}/reply, and GET /stats, while keeping the original stateless /process-ticket endpoint for the pipeline-inspector tool.
Introduced a measurable automation metric — added a get_today_stats() query that computes real-time ticket counts by outcome and an overall automation rate, turning "the system helps automate support" from a claim into a live, calculated number.
Debugged two real integration issues using tracebacks — resolved a stale-file routing error and a KeyError caused by an incomplete state-field refactor, both diagnosed from actual error tracebacks rather than guesswork.
Validated the decision logic against live requests — tested multiple real ticket scenarios (billing, technical, account-related) to confirm each of the three outcome paths triggers correctly, and calibrated the confidence threshold using the classifier's actual confidence distribution rather than an arbitrary number.
