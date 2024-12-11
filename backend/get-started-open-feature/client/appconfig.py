import traceback
from os import environ
from typing import Any, List, Union

from azure.appconfiguration.provider import load
from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential
from featuremanagement import FeatureManager, TargetingContext
from openfeature.client import (
    EvaluationContext,
    FlagEvaluationDetails,
    FlagEvaluationOptions,
    Hook,
    OpenFeatureClient,
)
from openfeature.exception import ErrorCode
from openfeature.flag_evaluation import FlagResolutionDetails, FlagType, Reason
from openfeature.provider import AbstractProvider, Metadata


class Config:
    def __init__(self, endpoint: str, credential: TokenCredential):
        self.endpoint = endpoint
        self.credential = credential


class AppConfigurationClient(OpenFeatureClient):
    def __init__(self, config: Config):
        self.endpoint = config.endpoint
        self.credential = config.credential

    def get_boolean_value(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: EvaluationContext | None,
        flag_evaluation_options: FlagEvaluationOptions | None,
    ) -> bool:
        return self.get_boolean_details(
            flag_key,
            default_value,
            evaluation_context,
            flag_evaluation_options,
        ).value

    def get_boolean_details(
        self,
        flag_key: str,
        default_value: bool,
        evaluation_context: EvaluationContext | None,
        flag_evaluation_options: FlagEvaluationOptions | None,
    ) -> FlagEvaluationDetails[bool]:
        return self.evaluate_flag_details(
            FlagType.BOOLEAN,
            flag_key,
            default_value,
            evaluation_context,
            flag_evaluation_options,
        )


class AppConfigurationProvider(AbstractProvider):
    def __init__(self, config: Config):
        self.config = config

    @property
    def client(self) -> AppConfigurationClient:
        return AppConfigurationClient()

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
    return AppConfigurationProvider(
        Config(
            endpoint=environ.get("APP_CONFIG_ENDPOINT"),
            credential=DefaultAzureCredential(),
        )
    )
