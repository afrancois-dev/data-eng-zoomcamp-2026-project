resource "google_service_account" "sa" {
  account_id   = var.account_id
  display_name = var.display_name
}

resource "google_project_iam_member" "sa_roles" {
  for_each = toset(var.roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.sa.email}"
}

variable "account_id" {
  type = string
}

variable "display_name" {
  type = string
}

variable "project_id" {
  type = string
}

variable "roles" {
  type    = list(string)
  default = []
}

output "email" {
  value = google_service_account.sa.email
}

output "name" {
  value = google_service_account.sa.name
}
