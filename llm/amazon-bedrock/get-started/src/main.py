import sys
from argparse import ArgumentParser

from mypy_boto3_bedrock import BedrockClient

from bedrock import get_bedrock_client, list_models


def get_options():
    parser = ArgumentParser()
    parser.add_argument(
        "command",
        metavar="cmd",
        type=str,
        help="Command to run. `list-motels`",
    )
    return parser.parse_args()


def print_models(client: BedrockClient):
    models = list_models(client)

    for model in models:
        print(f"Name: {model['modelName']}")
        print(f"ID: {model['modelId']}")
        print(f"ARN: {model['modelArn']}")
        print("---------------------")


if __name__ == "__main__":
    client = get_bedrock_client()

    options = get_options()
    if options.command == "list-models":
        print_models(client)
        sys.exit(0)
