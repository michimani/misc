<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.10.1 |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | =4.13.0 |
| <a name="requirement_launchdarkly"></a> [launchdarkly](#requirement\_launchdarkly) | ~> 2.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.13.0 |
| <a name="provider_launchdarkly"></a> [launchdarkly](#provider\_launchdarkly) | 2.21.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_app_configuration.main](https://registry.terraform.io/providers/hashicorp/azurerm/4.13.0/docs/resources/app_configuration) | resource |
| [azurerm_app_configuration_feature.feature](https://registry.terraform.io/providers/hashicorp/azurerm/4.13.0/docs/resources/app_configuration_feature) | resource |
| [azurerm_resource_group.main](https://registry.terraform.io/providers/hashicorp/azurerm/4.13.0/docs/resources/resource_group) | resource |
| [azurerm_role_assignment.appconfig_dataowner](https://registry.terraform.io/providers/hashicorp/azurerm/4.13.0/docs/resources/role_assignment) | resource |
| [launchdarkly_feature_flag.main](https://registry.terraform.io/providers/launchdarkly/launchdarkly/latest/docs/resources/feature_flag) | resource |
| [launchdarkly_feature_flag_environment.main](https://registry.terraform.io/providers/launchdarkly/launchdarkly/latest/docs/resources/feature_flag_environment) | resource |
| [launchdarkly_project.main](https://registry.terraform.io/providers/launchdarkly/launchdarkly/latest/docs/resources/project) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/4.13.0/docs/data-sources/client_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_azure_location"></a> [azure\_location](#input\_azure\_location) | The location/region where the Azure resources will be created. | `string` | `"Japan East"` | no |
| <a name="input_azure_subscription_id"></a> [azure\_subscription\_id](#input\_azure\_subscription\_id) | Azure subscription ID. | `string` | n/a | yes |
| <a name="input_launchdarkly_access_token"></a> [launchdarkly\_access\_token](#input\_launchdarkly\_access\_token) | LaunchDarkly access token. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_app_config_endpoint"></a> [app\_config\_endpoint](#output\_app\_config\_endpoint) | n/a |
<!-- END_TF_DOCS -->