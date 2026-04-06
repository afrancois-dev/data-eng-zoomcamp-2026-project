terraform {
  source = "${get_repo_root()}/iac/modules/workload-identity"
}

dependency "service_account" {
  config_path = "../service-account"
}

inputs = {
  pool_id               = "github-pool"
  pool_display_name     = "GitHub Workload Identity Pool"
  provider_id           = "github-provider"
  provider_display_name = "GitHub Provider"
  repository_name       = "afrancois-dev/data-eng-zoomcamp-2026-project"
  service_account_id    = dependency.service_account.outputs.mma_stats_sa_name
}
