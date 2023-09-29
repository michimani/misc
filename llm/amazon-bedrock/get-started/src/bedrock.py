import boto3
from mypy_boto3_bedrock import BedrockClient
from mypy_boto3_bedrock.type_defs import FoundationModelSummaryTypeDef


def get_bedrock_client() -> BedrockClient:
    return boto3.client(
        service_name="bedrock",
        region_name="us-east-1",
    )


def list_models(client: BedrockClient) -> list[FoundationModelSummaryTypeDef]:
    res = client.list_foundation_models()
    return res["modelSummaries"]
