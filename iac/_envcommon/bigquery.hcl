terraform {
  source = "${get_repo_root()}/iac/modules/bigquery"
}

inputs = {
  dataset_id                 = "mma_stats"
  description                = "Dataset for MMA stats project"
  location                   = "EU"
  delete_contents_on_destroy = true
}
