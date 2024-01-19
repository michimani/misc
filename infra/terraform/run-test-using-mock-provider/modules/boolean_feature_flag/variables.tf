locals {
  env = var.env

  bool_variations = {
    "true"  = true
    "false" = false
  }

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

variable "features" {
  type = map(object({
    description       = string
    default_variation = string
    overrides         = map(string)
  }))
  description = "List of boolean value features"
}
