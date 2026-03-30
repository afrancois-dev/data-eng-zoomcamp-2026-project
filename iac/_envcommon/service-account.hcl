terraform {
  source = "${get_repo_root()}/iac/modules/service-account"
}

inputs = {
  account_id   = "mma-stats-sa"
  display_name = "mma-stats Service Account"
  roles = [
    "roles/bigquery.admin",
    "roles/artifactregistry.admin",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin"
  ]
}
