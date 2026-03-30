locals {
  # common variables for all environments
  project_id  = "mma-stats-${local.environment}"
  region      = "europe-west1"
  repository  = "mma-stats" # for Artifact Registry
  image_name  = "mma-pipeline"

  # determine environment from directory structure
  environment = path_relative_to_include()
}

inputs = {
  project_id = local.project_id
  region     = local.region
}

# Generate GCP provider block
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "google" {
  project = "${local.project_id}"
  region  = "${local.region}"
}
EOF
}

# remote state on GCS (needs to be created manually)
remote_state {
  backend = "gcs"
  config = {
    bucket   = "${local.project_id}-terraform-state"
    prefix   = "${path_relative_to_include()}/terraform.state"
    location = local.region
    project  = local.project_id
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}
