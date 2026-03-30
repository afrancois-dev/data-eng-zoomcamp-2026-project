# MMA Stats - Data Engineering Project
[![Orchestration: Bruin](https://img.shields.io/badge/Orchestration-Bruin-orange)](https://getbruin.com)
[![Infrastructure: Terraform](https://img.shields.io/badge/Infrastructure-Terraform-623CE4)](https://terraform.io)

Final project for the **Data Engineering Zoomcamp 2026**. This platform ingests, transforms, and analyzes UFC statistics to provide insights and fight predictions.

## 🏗 Architecture
The architecture follows a **medallion-inspired lakehouse** pattern:
- **raw layer**: scraped data ingested directly into BigQuery.
- **staging layer**: cleaning, deduplication, and type casting via Bruin.
- **core layer (DWH)**: dimension and fact modeling (`dim_fighters`, `dim_events`, `fact_bouts`).

## 🛠 Stack
- **Orchestration**: [Bruin](https://getbruin.com) (SQL & Python assets) with Cloud Scheduler & Cloud Run
- **Data Warehouse**: BigQuery & DuckDB (local dev).
- **Infrastructure**: Terraform & Terragrunt.
- **Environments**: local, staging, production.
- **Security**: GitHub workload identity federation (keyless auth).

## 🚀 Quick Start

### 1. Prerequisites
```bash
pip install uv
curl -LsSf https://getbruin.com/install/cli | sh
uv sync --dev
```

### 2. Development Workflow
```bash
# Validate the pipeline
bruin validate app/

# Formatting
uv run ruff format
bruin format app/ --sqlfluff

# Local execution (DuckDB)
bruin run app/ --full-refresh
```

## 🌍 Infrastructure & Deployment

### Deployment with Terragrunt
```bash
cd iac/staging # or production
terragrunt run-all apply
```

### CI/CD Configuration (GitHub Actions)
The project uses **Workload Identity Federation**. Configure your GitHub environments with:
- 2 github repository environment (staging & production)
  - `GCP_WID_PROVIDER`
  - `GCP_SA_EMAIL`

## 📊 Data modeling
- **dim_fighters**: fighters (scd2)
- **dim_events**: events (scd2)
- **fact_bouts**: bouts containing (fact)

## 📝 Suggestions
- [ ] Streamlit dashboard for stats visualization.
- [ ] Slack webhook alerts for pipeline failures.
- [ ] Support for other organizations (hexagonemma, ares, pfl, ksw, Bellator).
- [ ] Gemini integration for predictive analysis.
