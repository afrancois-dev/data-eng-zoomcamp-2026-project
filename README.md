# MMA Stats - Data Engineering Project
[![Orchestration: Bruin](https://img.shields.io/badge/Orchestration-Bruin-orange)](https://getbruin.com)
[![Infrastructure: Terragrunt](https://img.shields.io/badge/Infrastructure-Terragrunt-4C51BF?logo=terraform&logoColor=white)](https://terragrunt.gruntwork.io/)
[![Cloud: GCP](https://img.shields.io/badge/Cloud-GCP-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![CI/CD: GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python: 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![DWH: BigQuery](https://img.shields.io/badge/DWH-BigQuery-669DF6?logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![DB: DuckDB](https://img.shields.io/badge/DB-DuckDB-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Storage: GCS](https://img.shields.io/badge/Storage-GCS-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/storage)
[![Compute: Cloud Run](https://img.shields.io/badge/Compute-Cloud_Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![Registry: Artifact Registry](https://img.shields.io/badge/Registry-Artifact_Registry-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/artifact-registry)
[![Scheduler: Cloud Scheduler](https://img.shields.io/badge/Scheduler-Cloud_Scheduler-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/scheduler)
[![Project: DE Zoomcamp](https://img.shields.io/badge/Project-DE%20Zoomcamp%202026-blue)](https://github.com/DataTalksClub/data-engineering-zoomcamp)

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

## 🚀 Quick start

### 1. Prerequisites
```bash
pip install uv
curl -LsSf https://getbruin.com/install/cli | sh
uv sync --dev
```

### 2. Development workflow
```bash
# source env
source .venv/bin/activate (within app/)

# validate the pipeline
bruin validate app/

# formatting
uv run ruff format
bruin format app/ --sqlfluff

# local execution (DuckDB)
bruin run app --full-refresh

# staging execution
bruin run app --environment staging
```

## 🌍 Infrastructure & deployment

### Deployment with Terragrunt
```bash
cd iac/staging # or production
terragrunt run -all apply
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

## Viz - Looker


## 📝 Suggestions
- [ ] Streamlit dashboard for stats visualization.
- [ ] Slack webhook alerts for pipeline failures.
- [ ] Support for other organizations (hexagonemma, ares, pfl, ksw, Bellator).
- [ ] Gemini integration for predictive analysis.
