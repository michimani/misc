locals {
  bool_variations = {
    "true"  = true
    "false" = false
  }

  domain_name = "${var.env}-${var.project_name}-os"

  tags = {
    env        = var.env
    managed_by = "terraform"
  }
}

variable "env" {
  type        = string
  description = "Environments short name"
}

variable "project_name" {
  type        = string
  description = "Project name"
}

variable "engine_version" {
  type        = string
  description = "OpenSearch version"
}

variable "instance_type" {
  type        = string
  description = "Instance type"
  default     = "t3.small.search"
}
