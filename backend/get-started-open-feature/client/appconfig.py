import traceback
from os import environ
from typing import Any, List, Union

from azure.appconfiguration.provider import load
from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential
from featuremanagement import FeatureManager, TargetingContext
from openfeature.client import (
    EvaluationContext,
    Hook,
)
from openfeature.exception import ErrorCode
from openfeature.flag_evaluation import (
    FlagResolutionDetails,
    FlagType,
    Reason,
)
from openfeature.provider import AbstractProvider, Metadata


class Config:
    """
    A class used to represent the configuration for connecting to a service.

    Attributes:
        endpoint : str
            The endpoint URL of the service.
        credential : TokenCredential
            The credential used for authentication.
    Methods:
        __init__(self, endpoint: str, credential: TokenCredential)
            Initializes the Config object with the given endpoint and credential.
    """

    def __init__(self, endpoint: str, credential: TokenCredential):
        self.endpoint = endpoint
        self.credential = credential


class AppConfigurationProvider(AbstractProvider):
    """
    AppConfigurationProvider is a feature flag provider that integrates with Azure App Configuration.

    Args:
        config (Config): Configuration object containing endpoint and credential information.
    Methods:
        get_metadata() -> Metadata:
            Returns metadata about the provider.
        get_provider_hooks() -> List[Hook]:
            Returns a list of hooks associated with the provider.
        resolve_boolean_details(flag_key: str, default_value: bool, evaluation_context: EvaluationContext | None) -> FlagResolutionDetails[bool]:
            Resolves the boolean flag value based on the provided flag key and evaluation context.
        resolve_string_details(flag_key: str, default_value: str, evaluation_context: EvaluationContext | None) -> FlagResolutionDetails[str]:
            Resolves the string flag value based on the provided flag key and evaluation context.
        resolve_integer_details(flag_key: str, default_value: int, evaluation_context: EvaluationContext | None) -> FlagResolutionDetails[int]:
            Resolves the integer flag value based on the provided flag key and evaluation context.
        resolve_float_details(flag_key: str, default_value: float, evaluation_context: EvaluationContext | None) -> FlagResolutionDetails[float]:
            Resolves the float flag value based on the provided flag key and evaluation context.
        resolve_object_details(flag_key: str, default_value: Union[dict, list], evaluation_context: EvaluationContext | None) -> FlagResolutionDetails[Union[dict, list]]:
            Resolves the object flag value based on the provided flag key and evaluation context.
    Private Methods:
        __resolve_value(flag_type: FlagType, flag_key: str, default_value: Any, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails:
            Internal method to resolve the flag value based on the flag type, flag key, and evaluation context.
    """

    def __init__(self, config: Config):
        self.config = config

    def get_metadata(self) -> Metadata:
        return Metadata("azure-app-configuration-server")

    def get_provider_hooks(self) -> List[Hook]:
        return []

    def resolve_boolean_details(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: EvaluationContext | None,
    ) -> FlagResolutionDetails[bool]:
        return self.__resolve_value(
            FlagType.BOOLEAN, flag_key, default_value, evaluation_context
        )

    def resolve_string_details(
        self,
        flag_key: str,
        default_value: str,
        evaluation_context: EvaluationContext | None,
    ) -> FlagResolutionDetails[str]:
        return FlagResolutionDetails(
            value=default_value,
            reason=Reason(Reason.ERROR),
            error_code=ErrorCode.TYPE_MISMATCH,
        )

    def resolve_integer_details(
        self,
        flag_key: str,
        default_value: int,
        evaluation_context: EvaluationContext | None,
    ) -> FlagResolutionDetails[int]:
        return FlagResolutionDetails(
            value=default_value,
            reason=Reason(Reason.ERROR),
            error_code=ErrorCode.TYPE_MISMATCH,
        )

    def resolve_float_details(
        self,
        flag_key: str,
        default_value: float,
        evaluation_context: EvaluationContext | None,
    ) -> FlagResolutionDetails[float]:
        return FlagResolutionDetails(
            value=default_value,
            reason=Reason(Reason.ERROR),
            error_code=ErrorCode.TYPE_MISMATCH,
        )

    def resolve_object_details(
        self,
        flag_key: str,
        default_value: Union[dict, list],
        evaluation_context: EvaluationContext | None,
    ) -> FlagResolutionDetails[Union[dict, list]]:
        return FlagResolutionDetails(
            value=default_value,
            reason=Reason(Reason.ERROR),
            error_code=ErrorCode.TYPE_MISMATCH,
        )

    def __resolve_value(
        self,
        flag_type: FlagType,
        flag_key: str,
        default_value: Any,
        evaluation_context: EvaluationContext | None = None,
    ) -> FlagResolutionDetails:
        if evaluation_context is None:
            return FlagResolutionDetails(
                value=default_value,
                reason=Reason(Reason.ERROR),
                error_code=ErrorCode.TARGETING_KEY_MISSING,
            )

        try:
            config_setting = load(
                endpoint=self.config.endpoint,
                credential=self.config.credential,
                feature_flag_enabled=True,
                feature_flag_refresh_enabled=True,
            )

            if config_setting is None:
                return FlagResolutionDetails(
                    value=default_value,
                    reason=Reason(Reason.ERROR),
                    error_code=ErrorCode.FLAG_NOT_FOUND,
                )

            feature_manager = FeatureManager(config_setting)
            enabled = feature_manager.is_enabled(
                flag_key, TargetingContext(user_id=evaluation_context.targeting_key)
            )

            return FlagResolutionDetails(
                value=enabled,
                reason=(Reason.TARGETING_MATCH if enabled else Reason.DISABLED),
            )

        except Exception:
            return FlagResolutionDetails(
                value=default_value,
                reason=Reason(Reason.ERROR),
                error_code=ErrorCode.PROVIDER_NOT_READY,
                error_message=f"Error occurred while resolving flag value. {traceback.format_exc()}",
            )


def init_provider() -> AppConfigurationProvider:
    """
    Initializes and returns an instance of AppConfigurationProvider.
    This function creates a new AppConfigurationProvider using the endpoint
    specified in the environment variable "APP_CONFIG_ENDPOINT" and the
    DefaultAzureCredential for authentication.

    Returns:
        AppConfigurationProvider: An instance of AppConfigurationProvider configured
        with the specified endpoint and credentials.
    """

    return AppConfigurationProvider(
        Config(
            endpoint=environ.get("APP_CONFIG_ENDPOINT"),
            credential=DefaultAzureCredential(),
        )
    )
