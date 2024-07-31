terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.80.0"
    }
  }
  required_version = "1.9.2"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "my-gke" {
  name     = "${var.project_id}-new-gke"
  location = var.region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Enable Istio
  addons_config {
    istio_config {
      disabled = false
      auth     = "AUTH_NONE"
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${google_container_cluster.my-gke.name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.my-gke.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-standard-8"
  }
}

resource "google_storage_bucket" "my-bucket" {
  name          = var.bucket
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}