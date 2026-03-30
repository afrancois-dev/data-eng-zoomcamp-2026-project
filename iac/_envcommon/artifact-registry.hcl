terraform {
  source = "tfr:///terraform-google-modules/repository/google//modules/repository?version=0.7.0"
}

inputs = {
  repository_id = "mma-stats"
  format        = "DOCKER"
  description   = "Docker repository for mma-stats pipeline"
}
