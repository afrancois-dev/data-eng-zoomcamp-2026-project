resource "google_service_account" "mma_stats_sa" {
  account_id   = "mma-stats-sa"
  display_name = "mma-stats Service Account"
}

resource "google_project_iam_member" "mma_stats_roles" {
  for_each = toset([
    "roles/bigquery.admin",
    "roles/artifactregistry.admin",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin"
  ])
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.mma_stats_sa.email}"
}

resource "google_service_account" "ui_sa" {
  account_id   = "mma-stats-ui-sa"
  display_name = "Streamlit UI Read-Only Service Account"
}

resource "google_project_iam_member" "ui_sa_roles" {
  for_each = toset([
    "roles/bigquery.jobUser",
    "roles/bigquery.dataViewer",
    "roles/bigquery.readSessionUser"
  ])
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.ui_sa.email}"
}

variable "project_id" {
  type = string
}

output "mma_stats_sa_email" {
  value = google_service_account.mma_stats_sa.email
}

output "mma_stats_sa_name" {
  value = google_service_account.mma_stats_sa.name
}

output "ui_sa_email" {
  value = google_service_account.ui_sa.email
}

output "ui_sa_name" {
  value = google_service_account.ui_sa.name
}
