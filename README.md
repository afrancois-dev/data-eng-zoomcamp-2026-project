# data-eng-zoomcamp-2026-project
Data engineering zoomcamp project - MMA stats

## NB 
- iac should be an external repository; for the sake of simplicity, I've included it in this project


## Set-up
- install uv
`pip install uv`

- install bruin
```
curl -LsSf https://getbruin.com/install/cli | sh
source ~/.bashrc
```
- install dependencies
`uv sync --dev`

- install bruin mcp (e.g on workspace)
```
{
  "servers": {
    "bruin": {
      "type": "stdio",
      "command": "bruin",
      "args": [
        "mcp"
      ]
    }
  },
  "inputs": []
}
```

## Useful devEx commands
typing
```
uv run ty check
```

linting and formating
```
uv run ruff check --fix # lint
uv run ruff format # formating
```

bruin format sql & assets def
```
uv run bruin format app/ --sqlfluff
```

bruin validate
```
bruin validate app/
```

install pre-commit
```
uv --directory app run prek install
```

## Debug commands

Query a dataset
```
bruin query --connection "duckdb-dev" --query "SELECT * FROM staging.fighters LIMIT 10" --description "Checking the content of staging.fighters table"
bruin query --connection duckdb-dev --query "SELECT count(*) FROM raw.bouts LIMIT 10"
bruin run app --tag bouts --exclude-tag raw # once raw has been exec. -> to avoid running too long
```

Run bruin based on tag : first load
```
bruin run app --full-refresh --tag fighters
bruin run app --full-refresh --tag events
bruin run app --full-refresh --tag bouts --debug
```

## NB
- I stored raw/ data on bigquery because the price is the same as gcs
- DWH
  - dim_fighters
    - I would have like to have a surrogate key not based on url, however; last_name can change for women when they are getting married. Also nickname is not a suitable candidate as it is not immutable
  - dim_events
    - location could change, date can also change -> url as the surrogate key

## IAC

Install terraform
```
Follow instruction on : https://developer.hashicorp.com/terraform/install
```

Install terragrunt (a wrapper for terraform)
```
curl -sL https://docs.terragrunt.com/install | bash
```

Gcloud auth login to be able to build GCP ressources
```
gcloud auth application-default login
```
NB: On GCP UI or console, don't forget to activate all needed services
- Google artifact
- IAM
- BigQuery
- ...

```
gcloud services enable iamcredentials.googleapis.com --project=mma-stats-staging
gcloud services enable run.googleapis.com --project mma-stats-staging 
...
```

Create ressources - terragrunt
```
terragrunt hcl fmt
cd iac/staging # (or iac/production)
terragrunt run -all plan
terragrunt run -all apply
```
NB: A docker image should be pushed to Artifact repository beforehand to create the cloud run job

## Docker (local)

Just for test purpose (to see whether the image is correctly built)
```
docker build -t mma-stats:test . && docker run --rm mma-stats:test --version
```

## CI/CD
- create 2 githbub repository environments
  - staging
    - fill GCP_WORKLOAD_IDENTITY_PROVIDER (go to GCP to see the value)
    - fill GCP_SERVICE_ACCOUNT : mma-stats-sa@mma-stats-staging.iam.gserviceaccount.com
  - production
    - fill GCP_WORKLOAD_IDENTITY_PROVIDER (go to GCP to see the value)
    - fill GCP_SERVICE_ACCOUNT : mma-stats-sa@mma-stats-staging.iam.gserviceaccount.com


