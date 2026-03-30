locals {
  # Load environment-level variables
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  # Extract out common variables for reuse
  environment = local.env_vars.locals.environment
  project_id  = local.env_vars.locals.project_id
  region      = "europe-west1"
  repository  = "mma-stats"
  image_name  = "mma-pipeline"
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
