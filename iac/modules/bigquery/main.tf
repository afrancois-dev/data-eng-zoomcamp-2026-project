resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset_id
  friendly_name               = var.dataset_id
  description                 = var.description
  location                    = var.location
  delete_contents_on_destroy  = var.delete_contents_on_destroy
}

variable "dataset_id" {
  type = string
}

variable "description" {
  type = string
}

variable "location" {
  type = string
}

variable "delete_contents_on_destroy" {
  type    = bool
  default = false
}

output "dataset_id" {
  value = google_bigquery_dataset.dataset.dataset_id
}
