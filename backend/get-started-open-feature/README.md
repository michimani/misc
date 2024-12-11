get started OpenFeature
===

## Requirements

### Accounts

- Azure
- LaunchDarkly

### Tools

- tfenv
  - `brew install tfenv`
- Azure CLI
  - `brew install az`
- LaunchDarkly CLI
  - `brew tap launchdarkly/homebrew-tap && brew install ldcli`

## Setup

1. Login to Azure and LaunchDarkly.

    ```sh
    az login
    ldcli login
    ```

2. Initialize Terraform and Python environment, and create feature flag on LaunchDarkly and Azure App Configuration.
   
   ```sh
   make init
   ```

3. Set environment variables.
  
    `client/.env` file is created by `make init` command. You can set environment variables in this file.

    ```sh
    LD_SDK_KEY='replace-with-your-sdk-key' 
    APP_CONFIG_ENDPOINT='replace-with-your-config-endpoint'
    ```
    
    The value of `LD_SDK_KEY` is the SDK key of LaunchDarkly. You can get it from the LaunchDarkly dashboard.
    
    The value of `APP_CONFIG_ENDPOINT` is the endpoint of Azure App Configuration. You can get it from the Azure portal or run the following command.
    
    ```sh
    cd infra \
    && terraform output -json | jq -r '.app_config_endpoint.value' \
    && cd -
    ```

## Usage

### Evaluate feature

```sh
make evaluate-feature
```

If you want to evaluate feature with specific user, you can specify user key.

```sh
make evaluate-feature ARGS='user-1'
```

### Clean up

Destroy all resources and python environment.

```sh
make clean
```

