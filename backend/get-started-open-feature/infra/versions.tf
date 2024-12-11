terraform {
  required_version = ">= 1.10.1"

  required_providers {
    # Azure
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.13.0"
    }

    # LaunchDarkly
    launchdarkly = {
      source  = "launchdarkly/launchdarkly"
      version = "~> 2.0"
    }
  }
}

provider "launchdarkly" {
  access_token = var.launchdarkly_access_token
}

provider "azurerm" {
  subscription_id = var.azure_subscription_id

  features {}
}
