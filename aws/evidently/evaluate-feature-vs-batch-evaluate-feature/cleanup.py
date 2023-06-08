from traceback import format_exc

import boto3

client = boto3.client("evidently")


def delete_project(name: str) -> bool:
    try:
        client.delete_project(project=name)
        print("Deleted project. name: {}".format(name))
        return True
    except:
        print("Failed to delete project. name: {}".format(name))
        print(format_exc())
        return False


def delete_feature(project: str, feature: str) -> bool:
    try:
        client.delete_feature(project=project, feature=feature)
        print("Deleted feature. name: {}".format(feature))
        return True
    except:
        print("Failed to delete feature. name: {}".format(feature))
        print(format_exc())
        return False


PROJECT_NAME: str = "ef-vs-bef"
FEATURE_NAME_BASE: str = "feature-{}"

if __name__ == "__main__":
    for i in range(0, 10):
        delete_feature(PROJECT_NAME, FEATURE_NAME_BASE.format(i + 1))

    delete_project(PROJECT_NAME)
