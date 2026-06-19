# NetworkOptCopilot: Project Plan and Architecture

## 1. Project Summary

**NetworkOptCopilot** is a full-stack decision-support platform for supply chain network optimization. The project combines data engineering, backend engineering, mathematical optimization, simulation, frontend visualization, and an LLM interpretation layer.

The project should be positioned as:

> **A Digital Twin and AI Decision-Support Platform for Inbound Supply Chain Network Optimization**

The system allows a user to define a supply chain network, run optimization and what-if simulations, inspect cost/service tradeoffs, identify bottlenecks, and ask natural-language questions about model results.

---

## 2. Target Use Case

The first target use case is an inbound or distribution network:

```text
Suppliers / Plants
      ↓
Cross-docks / Warehouses / DCs
      ↓
Customers / Demand points
```

The system should answer questions such as:

- What is the minimum-cost feasible flow through the network?
- Which lanes are fully utilized?
- Which nodes are bottlenecks?
- What happens if a DC loses 30% capacity?
- What is the cost impact of a demand surge?
- Which routes or modes are recommended?
- Why did one scenario cost more than another?
- What are the main drivers of cost, service risk, and operational complexity?

---

## 3. Alignment With Target Data Algorithm Engineer Role

This project aligns strongly with a role focused on supply chain optimization, digital twins, AI agents, and decision-support tools.

| Role Requirement | Project Component | Alignment |
|---|---|---|
| Inbound network design | Network flow optimization model | Strong |
| Cost and transit-time prediction | Future ML lane prediction module | Strong |
| Mode and route selection | Arc attributes: mode, cost, capacity, lead time | Strong |
| Consolidation strategies | Future hub/cross-dock and multi-stop scenarios | Strong |
| Digital Twin | Scenario-based network representation and UI | Strong |
| What-if simulation | Scenario cloning and optimization reruns | Very strong |
| Stress testing | Capacity loss, lane failure, demand surge scenarios | Very strong |
| Bottleneck detection | Binding constraints and utilization analysis | Very strong |
| ML lifecycle | Future pipelines, model evaluation, monitoring | To be added |
| Full-stack development | FastAPI + PostgreSQL + Next.js | Strong |
| APIs and UIs | REST API and dashboard | Strong |
| LLMs / AI agents | Result explainer and scenario builder | Strong |
| Docker / orchestration | Docker Compose now, Kubernetes later | Good trajectory |

---

## 4. System Architecture

### 4.1 Current Development Architecture

Current early-stage setup:

```text
WSL Ubuntu
│
├── Project code
│   └── ~/projects/NetworkOptCopilot
│
├── Backend
│   └── FastAPI running locally in Python virtual environment
│
└── Docker Compose
    └── PostgreSQL container
```

Current database connection:

```text
FastAPI local process
    ↓
localhost:5433
    ↓
Docker port forwarding
    ↓
PostgreSQL container port 5432
```

Current `DATABASE_URL`:

```env
DATABASE_URL=postgresql+psycopg://networkopt:networkopt@localhost:5433/networkopt
ENVIRONMENT=development
```

### 4.2 Target MVP Architecture

```text
Frontend
Next.js + TypeScript + React Flow
    ↓
Backend API
FastAPI + Pydantic + SQLAlchemy
    ↓
PostgreSQL
Projects, scenarios, nodes, arcs, runs, results
    ↓
Optimization Engine
Pyomo / OR-Tools / NetworkX
    ↓
LLM Layer
Explains results and creates structured scenario edits
```

### 4.3 Production-Like Architecture

```text
Frontend
Next.js dashboard, network graph, chat UI
    ↓
Backend API
FastAPI REST API
    ↓
PostgreSQL
Application data and optimization results
    ↓
Redis
Task broker and short-lived job status
    ↓
Celery Workers
Long-running optimization and simulation jobs
    ↓
Optimization Engine
Pyomo / OR-Tools / HiGHS / Gurobi later
    ↓
LLM Service
Scenario editor, result explainer, narrative generator
    ↓
Airflow + dbt
Scheduled ingestion, validation, feature engineering
    ↓
Monitoring
Logs, metrics, model performance, optimization runtime
```

---

## 5. Recommended Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js, TypeScript | Web application |
| UI graph | React Flow | Network visualization |
| Charts | Recharts / Plotly | KPI dashboards |
| Backend | FastAPI | REST API |
| Validation | Pydantic | Request and config validation |
| ORM | SQLAlchemy | Database models and queries |
| Migrations | Alembic | Database schema migrations |
| Database | PostgreSQL | Persistent application data |
| Async jobs | Celery + Redis | Background optimization jobs |
| Optimization | Pyomo, OR-Tools, NetworkX | Network flow and simulation |
| Solver | HiGHS initially, Gurobi later | Optimization solver |
| LLM | OpenAI API or local LLM | Explanations and scenario editing |
| Data pipelines | Airflow | Scheduled workflows |
| Transformations | dbt | Raw/staging/mart data modeling |
| Containerization | Docker Compose | Local services |
| Testing | pytest, FastAPI TestClient | Backend tests |

---

## 6. Repository Architecture

Recommended target structure:

```text
NetworkOptCopilot/
├── LICENSE
├── README.md
├── pyproject.toml
├── docker-compose.yml
├── .gitignore
├── .dockerignore
├── .env.example
│
├── backend/
│   ├── .env                  # ignored by Git
│   ├── .env.example          # safe template
│   ├── requirements.txt
│   ├── alembic.ini
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes_projects.py
│   │   │   ├── routes_scenarios.py
│   │   │   ├── routes_optimization.py
│   │   │   ├── routes_results.py
│   │   │   └── routes_chat.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   │
│   │   ├── models/
│   │   │   ├── project.py
│   │   │   ├── scenario.py
│   │   │   ├── node.py
│   │   │   ├── arc.py
│   │   │   ├── optimization_run.py
│   │   │   └── flow_result.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── project.py
│   │   │   ├── scenario.py
│   │   │   ├── network.py
│   │   │   └── optimization.py
│   │   │
│   │   ├── services/
│   │   │   ├── project_service.py
│   │   │   ├── scenario_service.py
│   │   │   ├── validation_service.py
│   │   │   ├── optimization_service.py
│   │   │   └── result_service.py
│   │   │
│   │   ├── optimization/
│   │   │   ├── min_cost_flow.py
│   │   │   ├── capacitated_flow.py
│   │   │   └── result_parser.py
│   │   │
│   │   ├── llm/
│   │   │   ├── client.py
│   │   │   ├── prompts.py
│   │   │   ├── result_explainer.py
│   │   │   └── scenario_editor.py
│   │   │
│   │   └── workers/
│   │       ├── celery_app.py
│   │       └── tasks.py
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │
│   └── tests/
│       └── test_health.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── data/
│   └── sample/
│       ├── nodes.csv
│       └── arcs.csv
│
├── pipelines/
│   ├── dags/
│   └── dbt/
│
└── docs/
    ├── architecture.md
    ├── data_model.md
    ├── optimization_model.md
    └── llm_layer.md
```

---

## 7. Git and Environment Hygiene

### 7.1 Required Rule

Before creating any `.env` file, make sure `.env` is ignored by Git.

`.gitignore` should include:

```gitignore
# Python
__pycache__/
*.pyc
.venv/

# Environment variables / secrets
.env
.env.*
!.env.example

# Node / Next.js
node_modules/
.next/
dist/
out/

# Local databases
*.db
*.sqlite
*.sqlite3
```

### 7.2 Environment Files

Use:

```text
backend/.env         # real local backend variables, ignored
.env.example         # safe project-level template, committed
backend/.env.example # optional backend-specific template, committed
```

Example `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://networkopt:networkopt@localhost:5433/networkopt
ENVIRONMENT=development
```

### 7.3 Why `.env.example` Exists

`.env.example` documents which variables the project needs without committing secrets.

A new developer can run:

```bash
cp backend/.env.example backend/.env
```

and then update real values locally.

---

## 8. Docker Compose Plan

### 8.1 Current Docker Compose

Current focus: PostgreSQL only.

```yaml
services:
  postgres:
    image: postgres:16
    container_name: networkopt_postgres
    environment:
      POSTGRES_DB: networkopt
      POSTGRES_USER: networkopt
      POSTGRES_PASSWORD: networkopt
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 8.2 Port Explanation

```yaml
ports:
  - "5433:5432"
```

means:

```text
host port 5433 → container port 5432
```

Current setup:

```text
localhost:5432 → local PostgreSQL installed in WSL
localhost:5433 → Docker PostgreSQL for NetworkOptCopilot
```

FastAPI running locally should use:

```env
DATABASE_URL=postgresql+psycopg://networkopt:networkopt@localhost:5433/networkopt
```

When FastAPI later runs inside Docker Compose, it should use:

```env
DATABASE_URL=postgresql+psycopg://networkopt:networkopt@postgres:5432/networkopt
```

### 8.3 Future Docker Compose Services

Later, add:

```text
redis
backend
worker
frontend
airflow
```

Redis is not required yet. It becomes useful when adding Celery background jobs.

---

## 9. Backend Plan

### 9.1 Current Backend

Current endpoints:

```text
GET /health
GET /db-health
```

Purpose:

- `/health`: confirms FastAPI is running.
- `/db-health`: confirms FastAPI can connect to PostgreSQL.

### 9.2 FastAPI App Responsibilities

The backend will eventually handle:

```text
Project CRUD
Scenario CRUD
Node and arc upload
Network validation
Optimization trigger
Optimization result retrieval
Scenario comparison
LLM chat and explanation
```

### 9.3 Backend Layers

```text
api/          HTTP route definitions
schemas/      Pydantic request and response models
models/       SQLAlchemy database models
services/     Business logic
optimization/ Solver logic
llm/          LLM prompts and orchestration
db/           Database session and base model
core/         Configuration and settings
workers/      Celery background tasks
```

---

## 10. Database Plan

### 10.1 Core Tables

#### `projects`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | text | Project name |
| description | text | Optional project description |
| created_at | timestamp | Creation time |

#### `scenarios`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| project_id | UUID | Foreign key to project |
| name | text | Scenario name |
| status | text | draft, ready, optimized, failed |
| created_at | timestamp | Creation time |

#### `nodes`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| scenario_id | UUID | Foreign key to scenario |
| node_code | text | Business identifier |
| node_type | text | plant, warehouse, dc, customer |
| supply_demand | float | Positive supply, negative demand |
| capacity | float | Node capacity |
| latitude | float | Optional |
| longitude | float | Optional |

#### `arcs`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| scenario_id | UUID | Foreign key to scenario |
| origin_node_id | UUID | Origin node |
| destination_node_id | UUID | Destination node |
| cost_per_unit | float | Transportation cost |
| capacity | float | Lane capacity |
| lead_time | float | Transit time |
| mode | text | truck, rail, air, ocean, etc. |

#### `optimization_runs`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| scenario_id | UUID | Scenario optimized |
| status | text | queued, running, completed, failed |
| solver_status | text | Solver status |
| objective_value | float | Total optimized cost |
| error_message | text | Failure details |
| created_at | timestamp | Creation time |
| completed_at | timestamp | Completion time |

#### `flow_results`

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| run_id | UUID | Optimization run |
| origin_node_id | UUID | Origin node |
| destination_node_id | UUID | Destination node |
| flow | float | Optimized flow |
| cost | float | Flow cost |
| utilization | float | Flow divided by capacity |

---

## 11. Migration Plan With Alembic

Alembic is the migration tool for SQLAlchemy, similar to Django migrations.

Workflow:

```text
Define SQLAlchemy model
    ↓
Generate migration
    ↓
Review migration script
    ↓
Apply migration to PostgreSQL
    ↓
Commit model and migration file
```

Commands:

```bash
alembic revision --autogenerate -m "create projects table"
alembic upgrade head
```

Expected Alembic files:

```text
backend/
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
```

---

## 12. Optimization Model Plan

### 12.1 First Model: Capacitated Minimum-Cost Flow

Sets:

```text
N = nodes
A = arcs
```

Parameters:

```text
c_ij = cost per unit on arc i,j
u_ij = capacity of arc i,j
b_i = net supply/demand at node i
```

Decision variable:

```text
x_ij = flow from node i to node j
```

Objective:

```text
minimize sum(c_ij * x_ij for all arcs)
```

Constraints:

```text
outflow_i - inflow_i = b_i
0 <= x_ij <= u_ij
```

### 12.2 Optimization Outputs

The solver should return:

```text
objective_value
flow by arc
cost by arc
utilization by arc
binding arcs
solver status
termination condition
```

---

## 13. Data Ingestion and Validation Plan

### 13.1 Input Files

`nodes.csv`:

```csv
node_code,node_type,supply_demand,capacity,latitude,longitude
P1,plant,1000,1000,42.36,-71.05
W1,warehouse,0,800,41.88,-87.62
C1,customer,-600,600,40.71,-74.00
C2,customer,-400,400,39.95,-75.16
```

`arcs.csv`:

```csv
origin,destination,cost_per_unit,capacity,lead_time,mode
P1,W1,2.5,800,2,truck
W1,C1,3.0,600,1,truck
W1,C2,2.8,500,1,truck
```

### 13.2 Validation Rules

Initial validation checks:

```text
No duplicate node codes
All arc origins exist
All arc destinations exist
No negative capacities
No negative costs
Total supply >= total demand
Demand nodes are reachable from supply nodes
No isolated demand nodes
```

---

## 14. LLM Layer Plan

The LLM should not solve the optimization problem. The LLM should explain, translate, and structure user intent.

### 14.1 Good LLM Responsibilities

```text
Summarize optimization results
Explain bottlenecks
Explain why a scenario is infeasible
Compare baseline and alternative scenarios
Convert natural-language edits into structured scenario changes
Generate executive summaries
```

### 14.2 Bad LLM Responsibilities

Avoid:

```text
Inventing numbers
Directly editing the database
Replacing the solver
Generating unvalidated SQL
Explaining results without retrieved facts
```

### 14.3 LLM Workflow

Example prompt:

> Why did scenario B cost more than baseline?

System workflow:

```text
Classify intent
    ↓
Retrieve baseline run results
    ↓
Retrieve scenario B run results
    ↓
Compute deterministic deltas
    ↓
Pass facts to LLM
    ↓
Generate grounded explanation
```

Example facts payload:

```json
{
  "baseline_total_cost": 120000,
  "scenario_total_cost": 135000,
  "delta": 15000,
  "delta_percent": 12.5,
  "main_driver": "W1 capacity reduction",
  "top_flow_changes": [
    {
      "arc": "P1-W2",
      "baseline_flow": 100,
      "new_flow": 400,
      "delta": 300
    }
  ]
}
```

---

## 15. Scenario Builder Plan

The user should eventually be able to ask:

```text
Increase C1 demand by 20%.
Close warehouse W1.
Reduce all truck capacity by 15%.
Add a lane from P2 to W2 with cost 3.5 and capacity 500.
```

Workflow:

```text
User prompt
    ↓
LLM extracts structured edit
    ↓
Backend validates edit
    ↓
Backend clones scenario
    ↓
Backend applies edit
    ↓
Optimization runs
    ↓
Results are compared and explained
```

Example structured edit:

```json
{
  "operation": "update_node",
  "target_type": "node",
  "target_code": "C1",
  "field": "supply_demand",
  "change_type": "percentage",
  "value": 20
}
```

---

## 16. Frontend Plan

Frontend stack:

```text
Next.js
TypeScript
React Flow
Recharts or Plotly
Tailwind CSS
```

Main screens:

```text
Project dashboard
Scenario dashboard
Network editor
CSV upload
Optimization run panel
Results dashboard
Scenario comparison
LLM chat interface
```

Key frontend components:

```text
ProjectList
ScenarioList
CsvUpload
NetworkGraph
OptimizationRunPanel
FlowResultsTable
CostBreakdownChart
ScenarioChat
```

---

## 17. Data Engineering Expansion

Add after MVP.

### 17.1 Airflow DAGs

Planned DAGs:

```text
network_data_ingestion_dag
network_data_validation_dag
nightly_baseline_optimization_dag
```

### 17.2 dbt Layers

Database schemas:

```text
raw
staging
marts
app
```

Example dbt models:

```text
stg_nodes.sql
stg_arcs.sql
int_network_connectivity.sql
mart_optimization_ready_network.sql
```

### 17.3 ML Feature Engineering

Future features:

```text
lane distance
mode
carrier
region
historical cost
historical transit time
lane volume
seasonality
service level
```

---

## 18. ML Layer Expansion

Add after optimization MVP.

### 18.1 Prediction Targets

```text
lane_cost
transit_time
service_risk
```

### 18.2 Models

Start with:

```text
linear regression baseline
random forest
gradient boosting
XGBoost or LightGBM later
```

### 18.3 Evaluation Metrics

```text
MAE
RMSE
MAPE
bias
prediction interval coverage
```

### 18.4 Realized vs Modeled Tracking

Store:

```text
predicted_cost
actual_cost
predicted_transit_time
actual_transit_time
prediction_error
model_version
```

---

## 19. Testing Plan

### 19.1 Current Tests

Current tests:

```text
GET /health
GET /db-health
```

### 19.2 Near-Term Tests

Add tests for:

```text
settings load correctly
database connection
project creation
scenario creation
node validation
arc validation
optimization solver on toy network
```

### 19.3 Test Categories

| Type | Purpose |
|---|---|
| Unit tests | Validate functions and services |
| API tests | Validate FastAPI endpoints |
| Integration tests | Validate database and solver connection |
| Solver tests | Validate optimization correctness |
| LLM tests | Validate structured output parsing |

---

## 20. MVP Roadmap

### Phase 1: Backend Foundation

```text
Docker PostgreSQL
FastAPI app
Database health check
pytest setup
Alembic setup
SQLAlchemy models
Project and scenario CRUD
```

### Phase 2: Network Data

```text
nodes table
arcs table
CSV upload
data validation
network retrieval API
```

### Phase 3: Optimization

```text
min-cost flow solver
optimization run table
flow results table
results retrieval API
```

### Phase 4: Frontend

```text
Next.js setup
project/scenario screens
CSV upload UI
result table
basic network visualization
```

### Phase 5: What-If Simulation

```text
scenario cloning
capacity/demand modifications
baseline vs scenario comparison
stress testing templates
```

### Phase 6: LLM Layer

```text
result summarizer
bottleneck explainer
scenario comparison explainer
structured scenario editor
```

### Phase 7: Data Engineering and MLOps

```text
Airflow
dbt
feature engineering
lane cost prediction
model evaluation
monitoring
```

---

## 21. Current Status

Current completed checkpoints:

```text
Project repository created
Docker Desktop + WSL integration working
PostgreSQL running through Docker Compose
PostgreSQL exposed on localhost:5433
FastAPI backend working
Database health endpoint working
pytest configured with pyproject.toml
2 backend tests passing
```

Current next step:

```text
Install and initialize Alembic
Configure Alembic to read backend/.env
Create SQLAlchemy Base
Create first models: Project and Scenario
Generate and apply first migration
```

---

## 22. Immediate Next Technical Steps

### Step A: Install Alembic

```bash
cd backend
source .venv/bin/activate
pip install alembic
pip freeze > requirements.txt
alembic init alembic
```

### Step B: Configure SQLAlchemy Base

Create:

```text
backend/app/db/base.py
```

Define:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

### Step C: Create Initial Models

Create:

```text
backend/app/models/project.py
backend/app/models/scenario.py
```

### Step D: Configure Alembic

Update:

```text
backend/alembic/env.py
```

to import:

```python
from app.db.base import Base
from app.models.project import Project
from app.models.scenario import Scenario
```

and set:

```python
target_metadata = Base.metadata
```

### Step E: Generate Migration

```bash
alembic revision --autogenerate -m "create projects and scenarios tables"
```

### Step F: Apply Migration

```bash
alembic upgrade head
```

### Step G: Verify Tables

```bash
psql -h localhost -p 5433 -U networkopt -d networkopt
```

Then:

```sql
\dt
```

Expected tables:

```text
projects
scenarios
alembic_version
```

---

## 23. Portfolio Positioning

Final positioning statement:

> **NetworkOptCopilot is a full-stack AI decision-support platform for inbound supply chain network optimization. It combines data pipelines, mathematical optimization, scenario simulation, and an LLM interpretation layer to support cost-service tradeoff analysis, bottleneck detection, and self-serve what-if simulation.**

This should be framed as a production-style supply chain digital twin, not merely a classroom optimization demo.

