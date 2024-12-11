resource "azurerm_resource_group" "main" {
  name     = "${local.project_name}-rg"
  location = var.azure_location
}

resource "azurerm_app_configuration" "main" {
  name                = "${local.project_name}-appconfig"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

data "azurerm_client_config" "current" {}

resource "azurerm_role_assignment" "appconfig_dataowner" {
  scope                = azurerm_app_configuration.main.id
  role_definition_name = "App Configuration Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_app_configuration_feature" "feature" {
  configuration_store_id = azurerm_app_configuration.main.id
  name                   = local.feature_name
  description            = "Feature flag for ${local.feature_name}"
  enabled                = true
  targeting_filter {
    default_rollout_percentage = 0
    users                      = ["user-1"]
  }

  depends_on = [
    azurerm_role_assignment.appconfig_dataowner,
  ]
}

output "app_config_endpoint" {
  value = azurerm_app_configuration.main.endpoint
}
