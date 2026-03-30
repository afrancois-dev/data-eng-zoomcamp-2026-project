resource "google_iam_workload_identity_pool" "pool" {
  workload_identity_pool_id = var.pool_id
  display_name               = var.pool_display_name
}

resource "google_iam_workload_identity_pool_provider" "gh_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.pool.workload_identity_pool_id
  workload_identity_pool_provider_id = var.provider_id
  display_name                       = var.provider_display_name

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository == '${var.repository_name}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "gh_sa_user" {
  service_account_id = var.service_account_id
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.pool.name}/attribute.repository/${var.repository_name}"
}

variable "pool_id" { type = string }
variable "pool_display_name" { type = string }
variable "provider_id" { type = string }
variable "provider_display_name" { type = string }
variable "service_account_id" { type = string }
variable "repository_name" { type = string }

output "provider_name" {
  value = google_iam_workload_identity_pool_provider.gh_provider.name
}
