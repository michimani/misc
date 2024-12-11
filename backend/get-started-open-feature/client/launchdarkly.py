from os import environ

from ld_openfeature import LaunchDarklyProvider
from ldclient import Config


def init_provider():
    sdk_key: str = environ.get("LD_SDK_KEY")
    return LaunchDarklyProvider(Config(sdk_key))
