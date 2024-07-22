variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The region to deploy the GKE cluster"
  type        = string
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
}

variable "node_count" {
  description = "The number of initial nodes in the cluster"
  type        = number
}

variable "machine_type" {
  description = "The machine type for the nodes in the cluster"
  type        = string
}
