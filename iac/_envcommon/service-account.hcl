terraform {
  source = "tfr:///terraform-google-modules/service-accounts/google//modules/simple-sa?version=4.2.0"
}

inputs = {
  name          = "mma-stats"
  display_name  = "mma-stats Service Account"
  description   = "Service account for the mma-stats data pipeline"
  project_roles = [
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/artifactregistry.writer",
    "roles/run.admin",
  ]
}
