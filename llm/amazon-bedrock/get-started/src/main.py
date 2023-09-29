import sys
from argparse import ArgumentParser

from mypy_boto3_bedrock import BedrockClient
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

from bedrock import (
    create_embedding,
    get_bedrock_client,
    get_bedrock_runtime_client,
    list_models,
)


def get_options():
    parser = ArgumentParser()
    parser.add_argument(
        "command",
        metavar="cmd",
        type=str,
        help="Command to run. `list-motels`",
    )
    parser.add_argument(
        "--input-text",
        type=str,
        help="Input text to create embedding for",
        default="Hello world",
    )
    return parser.parse_args()


def print_models(client: BedrockClient):
    models = list_models(client)

    for model in models:
        print(f"Name: {model['modelName']}")
        print(f"ID: {model['modelId']}")
        print(f"ARN: {model['modelArn']}")
        print("---------------------")


def print_embedding(client: BedrockRuntimeClient, input_text: str):
    embedding = create_embedding(client, input_text)
    print(f"Input text: {input_text}")
    print(f"Dimensions: {len(embedding)}")
    print(
        f"Embedding: [{embedding[0]}, {embedding[1]} ... {embedding[-2]}, {embedding[-1]}]"
    )


if __name__ == "__main__":
    options = get_options()

    if options.command == "list-models":
        client = get_bedrock_client()
        print_models(client)
        sys.exit(0)

    if options.command == "create-embedding":
        runtime_client = get_bedrock_runtime_client()
        print_embedding(runtime_client, options.input_text)
        sys.exit(0)
