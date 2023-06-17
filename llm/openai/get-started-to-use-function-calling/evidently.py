"""Evidently module for creating a new project and feature."""

from traceback import format_exc
from typing import Mapping, Optional, Tuple

from botocore.exceptions import BotoCoreError
from mypy_boto3_evidently import CloudWatchEvidentlyClient
from mypy_boto3_evidently.type_defs import (
    CreateFeatureResponseTypeDef,
    CreateProjectResponseTypeDef,
)


def project_exists(client: CloudWatchEvidentlyClient, project_name: str) -> bool:
    """Check if a project exists in evidently.

    Args:
        client (CloudWatchEvidentlyClient): The evidently client.
        project_name (str): The name of the project.

    Returns:
        bool: True if the project exists, False otherwise.
    """

    try:
        client.get_project(project=project_name)
    except BotoCoreError as botocore_error:
        print(botocore_error)
        return False
    except:  # pylint: disable=W0702
        print(format_exc())
        return False

    return True


def create_project(
    client: CloudWatchEvidentlyClient, project_name: str, project_description: str = ""
) -> Optional[str]:
    """Create a new project in evidently.

    Args:
        client (CloudWatchEvidentlyClient): The evidently client.
        project_name (str): The name of the project.
        project_description (str, optional): The description of the project. Defaults to "".

    Returns:
        Optional[str]: The ARN of the project if successful, None otherwise.
    """

    try:
        response: CreateProjectResponseTypeDef = client.create_project(
            name=project_name, description=project_description
        )
    except BotoCoreError as botocore_error:
        print(botocore_error)
        return None
    except:  # pylint: disable=W0702
        print(format_exc())
        return None

    return str(response["project"]["arn"])


def create_boolean_feature(
    client: CloudWatchEvidentlyClient,
    project_name: str,
    feature_name: str,
    feature_description: str = "",
    default_value: bool = False,
    override_rules: Optional[list[Tuple[str, str]]] = None,
) -> Optional[str]:
    """Create a new boolean feature in evidently.

    Args:
        client (CloudWatchEvidentlyClient): The evidently client.
        project_name (str): The name of the project.
        feature_name (str): The name of the feature.
        feature_description (str, optional): The description of the feature. Defaults to "".
        default_value (bool, optional): The default value of the feature. Defaults to False.
        override_rules (Optional[list[Tuple(str, str)]], optional): The override rules for
        the feature. Defaults to None.

    Returns:
        Optional[str]: The ARN of the feature if successful, None otherwise.
    """
    try:
        entity_override: Mapping[str, str] = {}
        for entity, variation in override_rules:
            entity_override[entity] = variation

        response: CreateFeatureResponseTypeDef = client.create_feature(
            project=project_name,
            name=feature_name,
            description=feature_description,
            variations=[
                {"name": "True", "value": {"boolValue": True}},
                {"name": "False", "value": {"boolValue": False}},
            ],
            defaultVariation=str(default_value),
            entityOverrides=entity_override,
        )
    except BotoCoreError as botocore_error:
        print(botocore_error)
        return None
    except:  # pylint: disable=W0702
        print(format_exc())
        return None

    return str(response["feature"]["arn"])
