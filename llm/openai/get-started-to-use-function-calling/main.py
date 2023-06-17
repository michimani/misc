import json
import sys
from traceback import format_exc
from typing import Final, Optional

import openai
from openai import ChatCompletion
from openai.error import InvalidRequestError

from function import CreateBooleanFeatureInput, create_evidently_boolean_feature

CHAT_MODEL_GPT35T_0613: Final[str] = "gpt-3.5-turbo-0613"


def run_chat(client: ChatCompletion, query: str) -> Optional[str]:
    """Run chat with GPT-3-turbo-0613 model to create Evidently Feature.

    Args:
        client (ChatCompletion): OpenAI ChatCompletion client.
        query (str): User query.

    Returns:
        Optional[str]: Response of create Evidently Feature.
    """

    try:
        response = client.create(
            model=CHAT_MODEL_GPT35T_0613,
            messages=[{"role": "user", "content": query}],
            functions=[
                {
                    "name": "create_evidently_boolean_feature",
                    "description": "Create a new boolean feature in evidently",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project_name": {
                                "type": "string",
                                "description": "Project name of CloudWatch Evidently.",
                            },
                            "feature_name": {
                                "type": "string",
                                "description": "Feature name of CloudWatch Evidently.",
                            },
                            "default_value": {
                                "type": "boolean",
                                "description": "Default value of CloudWatch Evidently.",
                                "default": False,
                            },
                            "override_rules": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                                "description": """Override rules of CloudWatch Evidently.
                                    This value is list of tuple that has two elements.
                                    First element is the name of entity,
                                    second element is the variation 'True' or 'False'.""",
                                "default": [],
                            },
                        },
                        "required": [
                            "project_name",
                            "feature_name",
                            "default_value",
                            "override_rules",
                        ],
                    },
                }
            ],
            function_call="auto",
        )
    except InvalidRequestError as ire:
        print(ire.__repr__())
        return None
    except:  # pylint: disable=W0702
        print(format_exc())
        return None

    params: CreateBooleanFeatureInput = __generate_calling_function_input(
        response.choices[0]["message"]
    )
    if params is None:
        print("Failed to create parameters for calling function.")
        return None

    __debug("params", params)

    create_res = create_evidently_boolean_feature(params)
    if not create_res:
        print("Failed to create a feature.")
        return None

    return f"""created a feature info

    Project: {params.project_name}
    Feature: {params.feature_name}

    Check the feature on CloudWatch Evidently using following command:

    aws evidently get-feature --project '{params.project_name}' --feature '{params.feature_name}'
    """


def __generate_calling_function_input(
    openai_message: dict,
) -> Optional[CreateBooleanFeatureInput]:
    __debug("openai_message", openai_message)

    if openai_message.get("function_call") is None:
        print("No function call.")
        return None

    print(f"function_call: {openai_message['function_call']['name']}")

    args_for_function = json.loads(openai_message["function_call"]["arguments"])

    override_rules = None
    if args_for_function.get("override_rules"):
        override_rules = [
            tuple(rule) for rule in args_for_function.get("override_rules")
        ]

    params = CreateBooleanFeatureInput(
        project_name=str(args_for_function.get("project_name")),
        feature_name=str(args_for_function.get("feature_name")),
        default_value=str(bool(args_for_function.get("default_value"))),
        override_rules=override_rules,
    )

    return params


def __debug(name: str, value: any):
    print(f"-------{name}-------")
    print(value)
    print("--------------------")


if __name__ == "__main__":
    message: str = ""
    while len(message) == 0:
        message = input("What do you want to create a feature? > ")

        if len(message) == 0:
            continue

        response_message = run_chat(
            client=openai.ChatCompletion,
            query=message,
        )

        if response_message is None:
            print("Failed to create a feature.")
            sys.exit(1)

        print("\n-------Response-------")
        print(response_message)
        sys.exit(0)
