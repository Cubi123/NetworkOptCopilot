# Project
NetworkOptCopilot is a learning-oriented supply chain optimization and digital twin project.

## Main rule
The user is learning step by step. Before editing files:
- Explain the plan.
- List files to change.
- Show the diff.
- Wait for approval unless explicitly told to edit.
Prefer small, reviewable changes.

## Commands

Start infrastructure:

docker compose up -d

Stop infrastructure:

docker compose down

Run backend:

cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

Run tests:

source backend/.venv/bin/activate
pytest -q

## Safety

Never commit:

.env
backend/.env
frontend/.env.local
gurobi.lic
API keys
tokens
passwords
private keys

## Specialized agents

Use detailed instructions from:

.codex/agents/testing.toml
.codex/agents/code-review.toml
.codex/agents/documentation.toml