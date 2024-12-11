locals {
  project_name = "open-feature-example"

  feature_name = "is_sushi"
}


variable "azure_location" {
  description = "The location/region where the Azure resources will be created."
  type        = string
  default     = "Japan East"
}

variable "launchdarkly_access_token" {
  description = "LaunchDarkly access token."
  type        = string
}

variable "azure_subscription_id" {
  description = "Azure subscription ID."
  type        = string
}
