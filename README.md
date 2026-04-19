# MMA Stats - Data Engineering Project
[![Cloud: GCP](https://img.shields.io/badge/Cloud-GCP-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Data Platform: Bruin](https://img.shields.io/badge/Dataplatform-Bruin-orange)](https://getbruin.com)
[![Orchestration: Cloud Scheduler](https://img.shields.io/badge/Orchestration-Cloud_Scheduler-4285F4?logo=clock&logoColor=white)](https://cloud.google.com/scheduler)
[![Infrastructure: Terragrunt](https://img.shields.io/badge/Infrastructure-Terragrunt-4C51BF?logo=terraform&logoColor=white)](https://terragrunt.gruntwork.io/)
[![CI/CD: GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python: 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![DWH: BigQuery](https://img.shields.io/badge/DWH-BigQuery-669DF6?logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![DB: DuckDB](https://img.shields.io/badge/DB-DuckDB-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Storage: GCS](https://img.shields.io/badge/Storage-GCS-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/storage)
[![Compute: Cloud Run](https://img.shields.io/badge/Compute-Cloud_Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![Registry: Artifact Registry](https://img.shields.io/badge/Registry-Artifact_Registry-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/artifact-registry)
[![Scheduler: Cloud Scheduler](https://img.shields.io/badge/Scheduler-Cloud_Scheduler-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/scheduler)
[![Project: DE Zoomcamp](https://img.shields.io/badge/Project-DE%20Zoomcamp%202026-blue)](https://github.com/DataTalksClub/data-engineering-zoomcamp)

Final project for the **Data Engineering Zoomcamp 2026**. This platform automates the ingestion, transformation, and analysis of UFC statistics to provide performance indicators and fight predictions based on historical data (next step by using Gemini).

## Problem description
Combat sports analysis, specifically for the UFC, often suffers from a lack of structured and accessible data for temporal analysis. This project solves this problem by:
- **centralizing** scattered UFC data (fighters, events, bout results) into a modern data warehouse.
- **modeling** fighter state changes (weight, rankings, record) via an SCD Type 2 approach to allow for accurate retrospective analysis.
- **automating** the end-to-end pipeline to offer decision-making dashboards for comparing fighting styles and predicting potential outcomes based on striking and grappling metrics.

## Architecture
The architecture follows a **medallion-inspired lakehouse** pattern:
- **raw layer**: raw data scraped via Python and injected directly into BigQuery (incremental mode).
- **staging layer**: cleaning, deduplication, and type casting via Bruin SQL.
- **core layer (DWH)**: dimensional modeling (fact/dim) with history management (SCD2).

## Tech stack
- **Orchestration**: [Bruin](https://getbruin.com) (SQL & Python assets) with cloud Scheduler & cloud Run.
- **data warehouse**: BigQuery (storage & compute) as the cost is the same as buckets.
- **infrastructure**: Terraform & Terragrunt for multi-environment management.
- **environments**: - local (DuckDB)
                    - staging (GCP)
                    - production (GCP)
- **security**: github workload identity federation (wif) for keyless authentication. Nowadays, it is too dangerous to generate a service account trough .json file.

## Quick start

### 1. Prerequisites
```bash
pip install uv
curl -LsSf https://getbruin.com/install/cli | sh
uv sync --dev
```

Install pre-commit (to get a production ready coding experience):
```bash
uv --directory app run prek install
```

Each time, you commit you will have this for instance
```
(ui) @afrancois-dev ➜ /workspaces/data-eng-zoomcamp-2026-project (staging) $ git commit -m "chore(README): update REAMDE.md"
Ruff Format..........................................(no files to check)Skipped
Ruff Lint............................................(no files to check)Skipped
Bruin Format sql files & asset definitions...............................Passed
Bruin Validate...........................................................Passed
Terragrunt Format........................................................Passed
```

### 2. Development workflow
```bash
# Source environment (within app/)
source .venv/bin/activate

# Validate the pipeline
bruin validate app/

# Formatting
uv run ruff format
bruin format app/ --sqlfluff

# Staging execution
bruin run app --environment staging
```

## Infrastructure and deployment

### Deployment with Terragrunt (i.e a terraform wrapper)
Infrastructure is fully automated via Terragrunt
```bash
cd iac/staging # or production
terragrunt run -all apply
```
*Note: Make sure to update the `project_id` in `.bruin.yml` and `iac/*/env.hcl`.*

### CI/CD Configuration (github actions)
The project uses **Workload identity federation**. Configure your github environments with:
- 2 environments (staging & production)
- required secrets:
  - `GCP_WID_PROVIDER`: WID provider identifier.
  - `GCP_SA_EMAIL`: Terraform service account email.

The [`.github/workflows/ci.yml`](.github/workflows/ci.yml) workflow automatically handles docker builds, pushing to artifact registry, and deploying to cloud Run.

## Data modeling and optimization (DWH)
The Data Warehouse is optimized for performance and cost:
- **dim_fighters**: Fighter dimension with history management (**SCD2**) using Bruin's `scd2_by_column` strategy.
- **dim_events**: Event dimension (SCD2).
- **fact_bouts**: Fact table containing bout results.
  - **Partitioning**: By day (`date`) to limit data scan for temporal queries.
  - **Clustering**: By `event_sk`, `fighter_1_sk`, `fighter_2_sk` to accelerate common joins and filters.

## Visualization
### Streamlit UI
An interactive interface to explore predictions. Generate a JSON key for your service account and use it through Streamlit Cloud.

### Looker Studio
The dashboard contains multiple analysis tiles (KO trends, performance by weight class, finish rates, etc.).
- [Link to Looker report](https://lookerstudio.google.com/reporting/4de86c35-f0fb-4b7c-9875-e29bf6c66181)

<img width="1214" height="770" alt="UFC Dashboard" src="https://github.com/user-attachments/assets/129c9be2-5894-4cad-9f08-0def727a8bc2" />

## Suggestions
- [ ] Slack webhook alerts for pipeline failures.
- [ ] Support for other organizations (hexagonemma, ares, pfl, ksw, Bellator). e.g inside raw/providers -> ares/ , ...
- [ ] Gemini integration for advanced predictive analysis.
