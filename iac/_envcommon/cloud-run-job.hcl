# this is an environment common configuration for Cloud Run Job
# it will be included in environmental terragrunt.hcl files.

dependency "artifact_registry" {
  config_path = "../artifact-registry"
}

dependency "service_account" {
  config_path = "../service-account"
}

terraform {
  source = "${get_repo_root()}/iac/modules/cloud-run-job"
}

inputs = {
  job_name = "mma-stats-pipeline"
  region   = "europe-west1"
  # We use the repository URL as a base, the initial version will be pushed via CI
  image_url             = "${dependency.artifact_registry.outputs.repository_url}/mma-stats:latest"
  service_account_email = dependency.service_account.outputs.email
}
