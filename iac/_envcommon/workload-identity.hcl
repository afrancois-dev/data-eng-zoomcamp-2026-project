terraform {
  source = "tfr:///terraform-google-modules/github-actions-runners/google//modules/gh-oidc?version=3.1.2"
}

inputs = {
  pool_id     = "github-actions-pool"
  provider_id = "github-actions-provider"
}
