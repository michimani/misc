import time
from traceback import format_exc
from typing import Final

import boto3

client: Final = boto3.client("evidently")


def list_features(project: str) -> list[str]:
    try:
        res = client.list_features(project=project)

        features = res.get("features")
        print("Listed features. count: {}".format(len(features)))
        return [feature.get("name") for feature in features]
    except:
        print("Failed to list features. project: {}".format(project))
        print(format_exc())
        return []


def get_all_feature_value_by_evaluate_feature(
    project: str, features: list[str], entity_id: str, debug: bool = False
):
    start = time.perf_counter()
    try:
        for feature in features:
            res = client.evaluate_feature(
                project=project, feature=feature, entityId=entity_id
            )
            if debug:
                print("feature: {}, value: {}".format(feature, res.get("value")))
    except:
        print("Failed to evaluate feature. project: {}".format(project))
        print(format_exc())

    end = time.perf_counter()
    print("elapsed: {}".format(end - start))


def get_all_feature_value_by_batch_evaluate_feature(
    project: str, features: list[str], entity_id: str, debug: bool = False
):
    start = time.perf_counter()
    try:
        requests = [{"feature": feature, "entityId": entity_id} for feature in features]
        res = client.batch_evaluate_feature(project=project, requests=requests)
        if debug:
            for result in res.get("results"):
                print(
                    "feature: {}, value: {}".format(
                        result.get("feature"), result.get("value")
                    )
                )
    except:
        print("Failed to batch evaluate feature. project: {}".format(project))
        print(format_exc())

    end = time.perf_counter()
    print("elapsed: {}".format(end - start))


PROJECT_NAME: Final[str] = "ef-vs-bef"
ENTITY_ID: Final[str] = "test-entity-id"


if __name__ == "__main__":
    features = list_features(PROJECT_NAME)

    print("\n\n---- get {} features by EvaluateFeature API ----".format(len(features)))
    for _ in range(0, 10):
        get_all_feature_value_by_evaluate_feature(
            project=PROJECT_NAME, features=features, entity_id=ENTITY_ID
        )

    print(
        "\n\n---- get {} features by BatchEvaluateFeature API ----".format(
            len(features)
        )
    )
    for _ in range(0, 10):
        get_all_feature_value_by_batch_evaluate_feature(
            project=PROJECT_NAME, features=features, entity_id=ENTITY_ID
        )
