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

install pre-commit
```
uv --directory app run prek install
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

# local execution (DuckDB) - deprecated because duckdb SQL is different from BigQuery
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
NB: Cloud scheduler has been automated via Terragrunt in the `cloud-run-job` module. It is launched every day (at 01:00 UTC).
NB 2: Update .bruin.yml project_id with your gcp project_id, and also make sure to modify iac/staging/env.hcl project_id.


Cloud Run deployed by terragrunt <br>
<img width="600" height="300" alt="Screenshot 2026-03-30 at 23 16 14" src="https://github.com/user-attachments/assets/237b5146-1855-4af7-9dc7-ea29dc9c510c" />

Cloud Scheduler (added manually -> btwn I am going to add it later to terragrunt. I was running out of time 😅)
<img width="600" height="230" alt="Screenshot 2026-03-30 at 23 23 46" src="https://github.com/user-attachments/assets/9a4d2cc8-4114-4c8f-8862-fc75cec1de2b" />



### CI/CD Configuration (GitHub Actions)
The project uses **Workload Identity Federation**. Configure your GitHub environments with:
- 2 github environments (staging & production)
  - with two secrets
    - `GCP_WID_PROVIDER`
    - `GCP_SA_EMAIL`

## 📊 Data modeling
- **dim_fighters**: fighters (scd2)
- **dim_events**: events (scd2)
- **fact_bouts**: bouts containing (fact)
<img width="593" height="324" alt="Screenshot 2026-03-30 at 23 15 22" src="https://github.com/user-attachments/assets/bc2bb435-a0e7-433e-9a36-e57d917e1d94" />


## Viz - Looker
- https://lookerstudio.google.com/reporting/4de86c35-f0fb-4b7c-9875-e29bf6c66181
<img width="1214" height="770" alt="Screenshot 2026-03-30 at 22 54 44" src="https://github.com/user-attachments/assets/129c9be2-5894-4cad-9f08-0def727a8bc2" />

## 📝 Suggestions
- [ ] Streamlit dashboard for stats visualization.
- [ ] Slack webhook alerts for pipeline failures.
- [ ] Support for other organizations (hexagonemma, ares, pfl, ksw, Bellator). e.g inside raw/providers -> ares/ 
- [ ] Gemini integration for predictive analysis.
