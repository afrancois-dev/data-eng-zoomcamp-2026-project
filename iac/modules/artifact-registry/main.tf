resource "google_artifact_registry_repository" "repo" {
  location      = var.location
  repository_id = var.repository_id
  format        = var.format
  description   = var.description
}

variable "location" {
  description = "The location of the repository"
  type        = string
}

variable "repository_id" {
  description = "The ID of the repository"
  type        = string
}

variable "format" {
  description = "The format of the repository"
  type        = string
}

variable "description" {
  description = "The description of the repository"
  type        = string
}

output "repository_id" {
  value = google_artifact_registry_repository.repo.repository_id
}
