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

Final project for the **Data Engineering Zoomcamp 2026**. This platform automates the ingestion, transformation, and analysis of UFC statistics to provide performance indicators and fight predictions based on historical data.

> *FYI: fight predictions will be included in a future iteration of the project using Gemini and function calling.*

<img width="2032" height="769" alt="mma-stats drawio" src="https://github.com/user-attachments/assets/674fddb7-02eb-446d-a5c2-47458092a082" />

## Problem description
Combat sports analysis, specifically for the UFC, often suffers from a lack of structured and accessible data for temporal analysis. This project solves this problem by:
- **centralizing** scattered UFC data (fighters, events, bout results) into a modern data warehouse.
- **modeling** fighter state changes (weight, rankings, record) via an SCD Type 2 approach to allow for accurate retrospective analysis.
- **automating** the end-to-end pipeline to offer decision-making dashboards for comparing fighting styles and predicting potential outcomes based on striking and grappling metrics.

## Architecture and data modeling
The project follows a **medallion-inspired lakehouse** pattern, managing the lineage and data flow through three distinct layers:

### Data lineage
Bruin automatically manage all the pipeline within the project:
- **raw/ layer**: python-based scrapers extract data directly from web sources into BigQuery tables (e.g., `raw.bouts`).
- **staging/ layer**: SQL transformations clean, cast, and deduplicate raw data while generating identifiers. `staging.bouts` depends on `raw.bouts`.
- **DWH layer (i.e core)**: dimensional models consolidate data for analysis. The `fact_bouts` table depends on `staging.bouts`, `dim_fighters`, and `dim_events` to ensure referential integrity.

<img width="1268" height="455" alt="Screenshot 2026-04-19 at 19 17 21" src="https://github.com/user-attachments/assets/f7be7d92-af3b-447d-8418-8a0bb43b98c0" />


### Modeling choices
The data warehouse uses a **star schema** optimized for BigQuery:
- **surrogate keys**: persistent identifiers are generated via a custom macro (using immutable source urls). This ensures stable joins across the pipeline. Most of the time, there were no suitable candidates to create a proper stable surrogate key; therefore, I used the URL as the SK. Additionally, I used `farm_fingerprint`, which is better as it returns a BIGINT instead of a hash.
- **SCD type 2**: All dimensions (`dim_fighters`, `dim_events`) implement **slowly changing dimension type 2** via Bruin's `scd2_by_column` strategy. This allows for point-in-time analysis (e.g., a fighter's weight class at the time of a specific historic fight). For `dim_fighters`, I would have loved to use a surrogate key based on (firstname, lastname); however, female fighters might change their last name when married, and duplicates are possible. Moreover, if I had fetched the fighter's birthday, it could have been a suitable SK.
- **fact table optimization**: The `fact_bouts` table is **partitioned by `date`** to reduce scan costs and **clustered by `event_sk` and `fighter_sk`** to accelerate common joins in downstream dashboards (even though the dataset is currently small, as I plan to add data from other providers, it is important to implement best practices for large-scale data to minimize technical debt).
- **incremental strategy**: All transformations use an incremental `time_interval` approach, processing only new data daily to minimize compute consumption. Additionally, in case a fighter fails a doping test and the bout's outcome changes (e.g., from a win to a no contest), we can simply re-fetch the data.

## Tech stack
- **Orchestration**: [Bruin](https://getbruin.com) (SQL & Python assets) with cloud Scheduler & cloud Run.
- **data warehouse**: BigQuery (storage & compute) as the cost is the same as buckets.
- **infrastructure**: Terraform & Terragrunt for multi-environment management.
- **environments**: - local (DuckDB)
                    - staging (GCP)
                    - production (GCP)
- **security**: github workload identity federation (wif) for keyless authentication. Nowadays, it is too dangerous to generate a service account through a .json file.

## Quick start

### 1. Prerequisites
```bash
pip install uv
curl -LsSf https://getbruin.com/install/cli | sh
uv sync --dev
```

Install pre-commit (to get a production-ready coding experience):
```bash
uv --directory app run prek install
```

Each time you commit, you will see this, for instance:
```
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
terragrunt run-all apply
```
*Note: Make sure to update the `project_id` in `.bruin.yml` and `iac/*/env.hcl`.*

### CI/CD Configuration (github actions)
The project uses **Workload identity federation**. Configure your github environments with:
- 2 environments (staging & production)
- required secrets:
  - `GCP_WID_PROVIDER`: WID provider identifier.
  - `GCP_SA_EMAIL`: Terraform service account email.

The [`.github/workflows/ci.yml`](.github/workflows/ci.yml) workflow automatically handles docker builds, pushing to artifact registry, and deploying to cloud Run.

## Visualization
### Streamlit UI
An interactive interface to explore data. Generate a JSON key for your service account and use it through Streamlit Cloud, otherwise; use the link below.
- https://mma-stats.streamlit.app/

### Looker Studio
The dashboard contains multiple analysis tiles (KO trends, performance by weight class, finish rates, etc.).
- [Link to Looker report](https://lookerstudio.google.com/reporting/4de86c35-f0fb-4b7c-9875-e29bf6c66181)

<img width="1214" height="770" alt="UFC Dashboard" src="https://github.com/user-attachments/assets/129c9be2-5894-4cad-9f08-0def727a8bc2" />

## Suggestions
- [ ] Slack webhook alerts for pipeline failures.
- [ ] Support for other organizations (hexagonemma, ares, pfl, ksw, Bellator). e.g inside raw/providers -> ares/ , ...
- [ ] Gemini integration for advanced predictive analysis.
