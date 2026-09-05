# AI Data Analyst Agent

An agentic AI data analyst that converts natural-language business questions into SQL, executes the SQL against PostgreSQL, and returns business-friendly answers.

The project is being built incrementally to understand how an Agentic AI system works in practice, starting with **LangChain + ChatOpenAI** and introducing **LangGraph only when the workflow requires explicit state, branching, retries, or more complex orchestration**.

---

## Current Capabilities

The current version can:

* Accept natural-language business questions
* Understand the database schema
* Generate SQL using an LLM
* Call a PostgreSQL execution tool
* Execute read-only SQL queries
* Pass database results back to the LLM
* Generate a business-friendly final answer
* Support tool-calling through LangChain

Example:

```text
User Question
      ↓
  ChatOpenAI
      ↓
  Tool Call
      ↓
 execute_sql
      ↓
 PostgreSQL
      ↓
 SQL Result
      ↓
  ChatOpenAI
      ↓
 Final Business Answer
```

---

## Architecture

```text
                    ┌─────────────────────┐
                    │    User Question    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ChatOpenAI      │
                    │                     │
                    │  Reasoning +        │
                    │  Tool Selection     │
                    └──────────┬──────────┘
                               │
                               │ Tool Call
                               ▼
                    ┌─────────────────────┐
                    │    execute_sql      │
                    │   LangChain Tool    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │      Database       │
                    └──────────┬──────────┘
                               │
                               │ Query Result
                               ▼
                    ┌─────────────────────┐
                    │     ChatOpenAI      │
                    │                     │
                    │  Result Analysis    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Final Answer     │
                    └─────────────────────┘
```

---

## Tech Stack

* **Python**
* **LangChain**
* **ChatOpenAI**
* **OpenAI GPT-5 Mini**
* **PostgreSQL 16**
* **SQLAlchemy**
* **psycopg2**
* **Docker**
* **uv**
* **VS Code**

LangGraph is intentionally not used in the current implementation. It will be introduced later when the agent requires more complex orchestration such as retries, validation loops, branching, or explicit state management.

---

## Project Structure

```text
ai-data-analyst/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── inventory.csv
│   └── monthly_demand.csv
│
├── docs/
│   └── data_dictionary.md
│
├── sql/
│   └── schema.sql
│
├── tests/
│   ├── test_tool_call.py
│   └── test_agent.py
│
├── src/
│   └── ai_data_analyst/
│       ├── __init__.py
│       ├── agent.py
│       ├── database.py
│       ├── llm.py
│       ├── model.py
│       ├── schema.py
│       ├── sql_generator.py
│       └── tools.py
│
├── .env
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Database

The project uses a synthetic analytics database in PostgreSQL.

### Tables

```text
customers
products
orders
order_items
inventory
monthly_demand
```

### Relationships

```text
customers
    │
    │ customer_id
    ▼
orders
    │
    │ order_id
    ▼
order_items
    │
    │ product_id
    ▼
products
    │
    ├──────────────► inventory
    │
    └──────────────► monthly_demand
```

### Revenue Definition

Revenue is calculated as:

```text
quantity × unit_price × (1 - discount)
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-data-analyst
```

### 2. Install dependencies

This project uses `uv`.

```bash
uv sync
```

If dependencies need to be added manually:

```bash
uv add langchain langchain-openai sqlalchemy psycopg2-binary python-dotenv
```

---

## 3. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://analyst:analyst_password@localhost:5432/analytics
OPENAI_API_KEY=your_openai_api_key
```

Never commit `.env` to Git.

Your `.gitignore` should contain:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## 4. Start PostgreSQL

The project uses Docker.

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker ps
```

You should see the PostgreSQL container:

```text
ai_analyst_postgres
```

---

## 5. Database Configuration

```text
Host:     localhost
Port:     5432
Database: analytics
User:     analyst
Password: analyst_password
```

---

## Agent Implementation

The core agent currently lives in:

```text
src/ai_data_analyst/agent.py
```

The LLM is connected to the SQL execution tool using LangChain:

```python
llm_with_tools = llm.bind_tools(
    [execute_sql]
)
```

This allows ChatOpenAI to decide when database access is required.

---

## SQL Tool

The SQL tool is defined in:

```text
src/ai_data_analyst/tools.py
```

It uses LangChain's `@tool` decorator:

```python
@tool
def execute_sql(query: str) -> list[dict]:
    ...
```

The tool executes the SQL against PostgreSQL and returns the results to the agent.

The current design is intended for read-only analytical queries.

---

## Testing

All project tests are located in the `tests/` directory.

### Test Tool Calling

Run:

```bash
uv run python tests/test_tool_call.py
```

This verifies that ChatOpenAI can recognize when the `execute_sql` tool is required and generate the appropriate tool call.

Example:

```text
User:
What are the number of customers?

        ↓

ChatOpenAI

        ↓

execute_sql

        ↓

SELECT COUNT(*) AS customer_count
FROM customers;
```

### Test the Agent

Run:

```bash
uv run python tests/test_agent.py
```

Example question:

```text
Which 5 products generated the most revenue?
```

The agent should:

1. Understand the question
2. Decide that database information is required
3. Generate an SQL tool call
4. Execute the SQL
5. Receive the database result
6. Generate a final business-friendly answer

---

## Current Agent Flow

```text
1. User asks a question
        ↓
2. ChatOpenAI receives the question
        ↓
3. LLM decides whether database information is required
        ↓
4. LLM generates an execute_sql tool call
        ↓
5. Python executes the tool
        ↓
6. PostgreSQL returns the result
        ↓
7. Result is sent back to ChatOpenAI
        ↓
8. ChatOpenAI generates the final answer
```

---

## Why This Is Agentic

This project is more than a simple:

```text
Question → SQL → Answer
```

pipeline.

The LLM has access to a tool and can decide whether that tool is required.

For example:

```text
Question:
"What are the number of customers?"

        ↓

ChatOpenAI

        ↓

Tool Call:
execute_sql(
    "SELECT COUNT(*) FROM customers"
)

        ↓

PostgreSQL

        ↓

Result:
300

        ↓

ChatOpenAI

        ↓

"There are 300 customers."
```

The important Agentic AI concept demonstrated here is **LLM-driven tool selection and execution**.

---

## Development Roadmap

### Phase 1 — Database

* [x] PostgreSQL setup
* [x] Docker PostgreSQL
* [x] Synthetic analytics dataset
* [x] Database schema
* [x] SQL exploration

### Phase 2 — Basic LLM → SQL

* [x] Natural-language question
* [x] SQL generation
* [x] PostgreSQL execution
* [x] Basic answer generation

### Phase 3 — LangChain Agent

* [x] ChatOpenAI integration
* [x] LangChain tools
* [x] `execute_sql` tool
* [x] Tool binding
* [x] Tool-call detection
* [x] Tool execution
* [x] Tool result → LLM
* [x] Final business answer

### Phase 4 — Agent Reliability

* [ ] SQL validation
* [ ] Read-only enforcement
* [ ] SQL error handling
* [ ] Self-correction
* [ ] Retry limits
* [ ] Prevent repeated tool calls
* [ ] Better query validation

### Phase 5 — Advanced Analysis

* [ ] Python analysis tool
* [ ] Pandas
* [ ] Charts
* [ ] Statistical analysis
* [ ] Multi-step analysis

### Phase 6 — Knowledge / RAG

* [ ] Business glossary
* [ ] Metric definitions
* [ ] RAG
* [ ] Semantic retrieval

### Phase 7 — Memory

* [ ] Conversation memory
* [ ] User context
* [ ] Follow-up questions

### Phase 8 — LangGraph

LangGraph will be introduced when the workflow requires:

* [ ] Explicit state
* [ ] Conditional branching
* [ ] Retry loops
* [ ] SQL validation → correction cycles
* [ ] Multiple agent/tool steps
* [ ] Complex orchestration

Example future workflow:

```text
                    ┌──────────────┐
                    │ User Question│
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Generate SQL │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Validate SQL │
                    └──────┬───────┘
                           ↓
                    ┌──────┴───────┐
                    │   Valid?     │
                    └──┬────────┬──┘
                      No        Yes
                       │          │
                       ↓          ↓
                ┌──────────┐  Execute
                │ Fix SQL  │     SQL
                └────┬─────┘      │
                     │            ↓
                     └──────► Analyze
                                  │
                                  ↓
                            Final Answer
```

---

## Project Goal

The goal is to build a production-oriented AI Data Analyst that can answer business questions over structured data while demonstrating core Agentic AI concepts:

* LLM reasoning
* Tool calling
* SQL generation
* Database interaction
* SQL validation
* Error recovery
* Multi-step reasoning
* State management
* RAG
* Memory
* Evaluation
* Production API architecture

The project is intentionally being developed **step by step**, with each layer added only when the previous layer is understood and working.
