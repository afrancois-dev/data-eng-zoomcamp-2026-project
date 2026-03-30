include "root" {
  path = find_in_parent_folders("root.hcl")
}

include "envcommon" {
  path = "${get_terragrunt_dir()}/../../_envcommon/workload-identity.hcl"
}

dependency "service_account" {
  config_path = "../service-account"
}

inputs = {
  service_account_id = dependency.service_account.outputs.name
  sa_mappings = {
    "mma-stats" = {
      sa_name   = dependency.service_account.outputs.email
      attribute = "attribute.repository/afrancois-dev/data-eng-zoomcamp-2026-project:ref/refs/heads/production"
    }
  }
}
