"""Functions for Evidently feature flagging."""

from typing import Optional, Tuple

import boto3
from pydantic.dataclasses import dataclass

import evidently

client = boto3.client("evidently")


@dataclass
class CreateBooleanFeatureInput:
    """Input for create_evidently_boolean_feature function."""

    project_name: str
    feature_name: str
    default_value: bool = False
    override_rules: Optional[list[Tuple[str, str]]] = None


def create_evidently_boolean_feature(params: CreateBooleanFeatureInput) -> bool:
    """Create a new boolean feature in evidently.

    Args:
        params (CreateBooleanFeatureInput): The input parameters.

    Returns:
        bool: True if successful, False otherwise.
    """

    if not evidently.project_exists(client, params.project_name):
        project_arn = evidently.create_project(client, params.project_name)
        if project_arn is None:
            print("Failed to create project")
            return False

        print(f"Created project {params.project_name} with ARN {project_arn}")

    feature_arn = evidently.create_boolean_feature(
        client,
        params.project_name,
        params.feature_name,
        default_value=params.default_value,
        override_rules=params.override_rules,
    )

    if feature_arn is None:
        print("Failed to create feature")
        return False

    print(f"Created feature {params.feature_name} with ARN {feature_arn}")
    return True
