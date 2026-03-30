variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy the Cloud Run Job"
  type        = string
}

variable "job_name" {
  description = "The name of the Cloud Run Job"
  type        = string
}

variable "image_url" {
  description = "The full URL of the Docker image"
  type        = string
}

variable "service_account_email" {
  description = "The service account email to run the job"
  type        = string
}

resource "google_cloud_run_v2_job" "default" {
  name     = var.job_name
  location = var.region
  
  deletion_protection = false

  template {
    template {
      service_account = var.service_account_email
      containers {
        image = var.image_url
        
        # Default Bruin command
        args = ["run", ".", "--environment", trimprefix(var.project_id, "mma-stats-")]

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].template[0].containers[0].image,
    ]
  }
}

output "job_name" {
  value = google_cloud_run_v2_job.default.name
}

output "job_url" {
  value = google_cloud_run_v2_job.default.terminal_condition[0].type
}
