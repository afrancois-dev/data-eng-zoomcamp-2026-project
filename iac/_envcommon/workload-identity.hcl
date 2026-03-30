terraform {
  source = "${get_repo_root()}/iac/modules/workload-identity"
}

inputs = {
  pool_id               = "github-pool"
  pool_display_name     = "GitHub Workload Identity Pool"
  provider_id           = "github-provider"
  provider_display_name = "GitHub Provider"
  repository_name       = "afrancois-dev/data-eng-zoomcamp-2026-project"
  # service_account_id sera passé via dependency dans les dossiers staging/prod
}
