# DataPulse-AI 📊🤖

An automated enterprise-level workforce data pipeline engineered to mirror the operational lifecycle challenges found within the **Affirm AI Solutions Engineer** profile. This system ingests unstructured operational logs, models them through a containerized database layer, and orchestrates frontier AI agents to identify compliance risks automatically.

## 🛠️ The Enterprise Stack
* **Backend Framework:** FastAPI (Asynchronous Python)
* **Data Layer / Warehouse:** PostgreSQL (Containerized via Docker)
* **Data Transformation:** dbt Core
* **AI Orchestration:** Anthropic Claude API / OpenAI API
* **Deployment Validation:** Docker Compose

# DataPulse-AI 📊🤖

An automated enterprise-level workforce data pipeline engineered to mirror the operational lifecycle challenges found within the **Affirm AI Solutions Engineer** profile. This system ingests unstructured operational logs, models them through a containerized database layer, and orchestrates frontier AI agents to identify compliance risks automatically.

## 🛠️ The Enterprise Stack
* **Backend Framework:** FastAPI (Asynchronous Python)
* **Data Layer / Warehouse:** PostgreSQL (Containerized via Docker)
* **Data Transformation:** dbt Core
* **AI Orchestration:** Anthropic Claude API / OpenAI API
* **Deployment Validation:** Docker Compose

## 🚀 Architectural Setup
1. **Infrastructure Initialization:** Spin up the localized PostgreSQL instance:
   ```bash
   docker compose up -d
   ```
2. **Environment Insulation:** Configure your local secure variables inside `.env`.
3. **Database Seeding:** Populate your enterprise data storage layer with mock workforce profiles:
   ```bash
   python backend/app/seed_db.py
   ```

