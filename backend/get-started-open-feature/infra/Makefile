LAUNCHDARKLY_ACCESS_TOKEN := $(shell ldcli config --list --output json | jq -r '."access-token"')
AZURE_SUBSCRIPTION_ID := $(shell az account show --query 'id' --output tsv)

init:
	tfenv install \
	&& terraform init -upgrade

plan:
	terraform fmt ./ \
	&& terraform plan -var="azure_subscription_id=$(AZURE_SUBSCRIPTION_ID)" -var="launchdarkly_access_token=$(LAUNCHDARKLY_ACCESS_TOKEN)"

apply:
	terraform fmt ./ \
	&& terraform apply  -var="azure_subscription_id=$(AZURE_SUBSCRIPTION_ID)" -var="launchdarkly_access_token=$(LAUNCHDARKLY_ACCESS_TOKEN)" -auto-approve

clean:
	cd infra \
	&& terraform -var="azure_subscription_id=$(AZURE_SUBSCRIPTION_ID)" -var="launchdarkly_access_token=$(LAUNCHDARKLY_ACCESS_TOKEN)" destroy