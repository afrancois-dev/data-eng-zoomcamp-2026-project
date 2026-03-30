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
bruin run app --full-refresh -> run all
```

Test connections
```
# list all connections
bruin connections list

# test connection
bruin connections test --name db --environment staging
```

Run bruin on staging (:warning: --full-refresh for the first load)
```
bruin run app --environment staging --full-refresh
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

## Streamlit


## Run example
```
@afrancois-dev ➜ /workspaces/data-eng-zoomcamp-2026-project (staging) $ bruin run app --full-refresh
Analyzed the pipeline 'mma-stats' with 9 assets.

Pipeline: mma-stats (.)
  No issues found

✓ Successfully validated 9 assets across 1 pipeline, all good.

Interval: 2026-03-29T00:00:00Z - 2026-03-29T23:59:59Z

Starting the pipeline execution...

[14:39:06] Running:  raw.events
[14:39:06] Running:  raw.fighters
[14:39:06] [raw.fighters] >> Resolved 126 packages in 1ms
[14:39:06] [raw.events] >> Resolved 126 packages in 1ms
[14:39:08] [raw.events] Successfully collected the data from the asset, uploading to the destination...
[14:39:10] [raw.events] Successfully loaded the data from the asset into the destination.
[14:39:10] Finished: raw.events (4.545s)
[14:39:10] Running:  staging.events
[14:39:10] Running:  raw.events:metadata-push
[14:39:10] Finished: raw.events:metadata-push (0s)
[14:39:11] Finished: staging.events (67ms)
[14:39:11] Running:  staging.events:metadata-push
[14:39:11] Finished: staging.events:metadata-push (0s)
[14:39:11] Running:  staging.events:id:not_null
[14:39:11] Running:  staging.events:name:unique
[14:39:11] Running:  staging.events:id:unique
[14:39:11] Running:  staging.events:name:not_null
[14:39:11] Running:  staging.events:date:not_null
[14:39:11] Running:  staging.events:location:not_null
[14:39:11] Finished: staging.events:id:not_null (20ms)
[14:39:11] Finished: staging.events:name:unique (54ms)
[14:39:11] Finished: staging.events:date:not_null (79ms)
[14:39:11] Finished: staging.events:name:not_null (101ms)
[14:39:11] Finished: staging.events:id:unique (116ms)
[14:39:11] Finished: staging.events:location:not_null (133ms)
[14:39:11] Running:  dwh.dim_events
[14:39:11] Finished: dwh.dim_events (67ms)
[14:39:11] Running:  dwh.dim_events:metadata-push
[14:39:11] Finished: dwh.dim_events:metadata-push (0s)
[14:39:28] [raw.fighters] Successfully collected the data from the asset, uploading to the destination...
[14:39:30] [raw.fighters] Successfully loaded the data from the asset into the destination.
[14:39:30] Finished: raw.fighters (24.143s)
[14:39:30] Running:  staging.fighters
[14:39:30] Running:  raw.bouts
[14:39:30] Running:  raw.fighters:metadata-push
[14:39:30] Finished: raw.fighters:metadata-push (0s)
[14:39:30] [raw.bouts] >> Resolved 126 packages in 2ms
[14:39:30] Finished: staging.fighters (91ms)
[14:39:30] Running:  staging.fighters:metadata-push
[14:39:30] Finished: staging.fighters:metadata-push (0s)
[14:39:30] Running:  staging.fighters:id:not_null
[14:39:30] Running:  staging.fighters:last_name:not_null
[14:39:30] Running:  staging.fighters:first_name:not_null
[14:39:30] Running:  staging.fighters:wins:min
[14:39:30] Finished: staging.fighters:id:not_null (20ms)
[14:39:30] Finished: staging.fighters:first_name:not_null (45ms)
[14:39:30] Finished: staging.fighters:wins:min (76ms)
[14:39:30] Finished: staging.fighters:last_name:not_null (95ms)
[14:39:30] Running:  dwh.dim_fighters
[14:39:30] Finished: dwh.dim_fighters (68ms)
[14:39:30] Running:  dwh.dim_fighters:metadata-push
[14:39:30] Finished: dwh.dim_fighters:metadata-push (0s)
[15:00:13] [raw.bouts] Successfully collected the data from the asset, uploading to the destination...
[15:00:16] [raw.bouts] Successfully loaded the data from the asset into the destination.
[15:00:16] Finished: raw.bouts (20m45.659s)
[15:00:16] Running:  staging.bouts
[15:00:16] Running:  raw.bouts:metadata-push
[15:00:16] Finished: raw.bouts:metadata-push (0s)
[15:00:16] Finished: staging.bouts (113ms)
[15:00:16] Running:  staging.bouts:metadata-push
[15:00:16] Finished: staging.bouts:metadata-push (0s)
[15:00:16] Running:  staging.bouts:bout_id:not_null
[15:00:16] Running:  staging.bouts:date:not_null
[15:00:16] Running:  staging.bouts:event_id:not_null
[15:00:16] Running:  staging.bouts:fighter_1_id:not_null
[15:00:16] Running:  staging.bouts:fighter_2_id:not_null
[15:00:16] Finished: staging.bouts:bout_id:not_null (15ms)
[15:00:16] Finished: staging.bouts:event_id:not_null (30ms)
[15:00:16] Finished: staging.bouts:fighter_2_id:not_null (44ms)
[15:00:16] Finished: staging.bouts:date:not_null (58ms)
[15:00:16] Finished: staging.bouts:fighter_1_id:not_null (74ms)
[15:00:16] Running:  dwh.fact_bouts
[15:00:16] Finished: dwh.fact_bouts (107ms)
[15:00:16] Running:  dwh.fact_bouts:metadata-push
[15:00:16] Finished: dwh.fact_bouts:metadata-push (0s)

==================================================

PASS raw.events 
PASS staging.events ......
PASS dwh.dim_events 
PASS raw.fighters 
PASS staging.fighters ....
PASS dwh.dim_fighters 
PASS raw.bouts 
PASS staging.bouts .....
PASS dwh.fact_bouts 


bruin run completed successfully in 21m10.099s

 ✓ Assets executed      9 succeeded
 ✓ Quality checks       15 succeeded
 ✓ Metadata pushed      9
```


## Suggestions - next steps
- use a slack channel webhook to get pipeline alerts
- use datadog to get logs info (maybe overkill) at this moment for such this app
- add other providers than ufc (i.e hexagonemma, ares, bellator,...)
- connect a gemini / langchain agent
- get realtime data
- get feeds from X
- move iac folder to another repository
- move streamlit folder to another repository
- add a map based on location event