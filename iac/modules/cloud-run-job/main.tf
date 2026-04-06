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
  # only used for 1st deployment as the ci did not push the image yet
  default     = "hello-world"
}

variable "service_account_email" {
  description = "The service account email to run the job"
  type        = string
}

variable "schedule" {
  description = "The cron schedule for the job"
  type        = string
  default     = "0 1 * * *"
}

resource "google_cloud_run_v2_job" "default" {
  name     = var.job_name
  location = var.region
  
  deletion_protection = false

  template {
    template {
      # we let bruin retry on its side
      max_retries     = 0
      service_account = var.service_account_email
      containers {
        image = var.image_url
        # by default, bruin runs for D-1 if no dates are provided.
        # i.e daily scheduling at 01:00 UTC to pick up D-1 data.
        args = ["run", ".", "--environment", trimprefix(var.project_id, "mma-stats-"), "--push-metadata"]

        resources {
          limits = {
            cpu    = "1"
            memory = "4Gi"
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

resource "google_cloud_scheduler_job" "job_scheduler" {
  name             = "${var.job_name}-scheduler"
  description      = "Trigger for ${var.job_name} Cloud Run Job"
  schedule         = var.schedule
  time_zone        = "UTC"
  attempt_deadline = "320s"
  region           = var.region
  project          = var.project_id

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.default.name}:run"

    oauth_token {
      service_account_email = var.service_account_email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}

output "job_name" {
  value = google_cloud_run_v2_job.default.name
}

output "job_url" {
  value = google_cloud_run_v2_job.default.terminal_condition[0].type
}
