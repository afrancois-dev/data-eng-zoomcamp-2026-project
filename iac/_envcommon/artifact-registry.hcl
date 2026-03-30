terraform {
  source = "${get_repo_root()}/iac/modules/artifact-registry"
}

inputs = {
  repository_id = "mma-stats"
  format        = "DOCKER"
  description   = "Docker repository for mma-stats pipeline"
  location      = "europe-west1"
}
