from traceback import format_exc
from typing import Final

import boto3

client = boto3.client("evidently")


def create_project(name: str) -> bool:
    try:
        res = client.create_project(name=name)

        created = res.get("project")
        print("Created project. name: {}".format(created.get("name")))
        return True
    except:
        print("Failed to create project. name: {}".format(name))
        print(format_exc())
        return False


def create_feature(project: str, feature: str) -> bool:
    try:
        res = client.create_feature(
            project=project,
            name=feature,
            variations=[
                {"name": "true", "value": {"boolValue": True}},
                {"name": "false", "value": {"boolValue": False}},
            ],
            defaultVariation="true",
        )

        created = res.get("feature")
        print("Created feature. name: {}".format(created.get("name")))
        return True
    except:
        print("Failed to create feature. name: {}".format(feature))
        print(format_exc())
        return False


PROJECT_NAME: Final[str] = "ef-vs-bef"
FEATURE_NAME_BASE: Final[str] = "feature-{}"

if __name__ == "__main__":
    if create_project(PROJECT_NAME):
        for i in range(0, 10):
            create_feature(PROJECT_NAME, FEATURE_NAME_BASE.format(i + 1))
