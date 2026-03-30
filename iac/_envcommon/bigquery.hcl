terraform {
  source = "tfr:///terraform-google-modules/bigquery/google//modules/bigquery?version=7.0.0"
}

inputs = {
  dataset_id   = "mma_stats"
  location     = "europe-west1"
}
