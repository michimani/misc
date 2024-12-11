import sys
from os import environ
from pprint import pprint as pp

from openfeature import api
from openfeature.client import OpenFeatureClient
from openfeature.evaluation_context import EvaluationContext

import appconfig as ac
import launchdarkly as ld

FEATURE_NAME: str = "is_sushi"


def main(user_id: str) -> int:
    # init OpenFeature provider
    # provider = ld.init_provider()
    provider = ac.init_provider()

    api.set_provider(provider)

    client: OpenFeatureClient = api.get_client()

    # check if feature is enabled
    detail = client.get_boolean_details(
        flag_key=FEATURE_NAME,
        default_value=False,
        evaluation_context=EvaluationContext(
            targeting_key=user_id,
            attributes={},
        ),
    )

    pp(detail)

    return 0


if __name__ == "__main__":
    user_id: str = "user-0"

    args = sys.argv
    if len(args) > 1:
        user_id = args[1]

    sys.exit(main(user_id=user_id))
