import inspect
import os
from typing import Any, Type, Union

from ...base import LLMClient, get_llm, register_llm
from ...types import LLMResponse


@register_llm("auto_from_env")
class AutoFromEnvLLMClient(LLMClient):
    """
    Select a registered provider from environment variables.

    Environment variables:
        - LLM_PROVIDER: the corresponding name in the LLMClient registry
          (defaults to "litellm")
        - MODEL_NAME: model name or id used by the selected provider
    """

    def __init__(self) -> None:
        provider_name = os.getenv("LLM_PROVIDER", "litellm")
        self.model_name = os.getenv("MODEL_NAME")
        self.model_name_in_generate = False

        provider_type = get_llm(provider_name)
        init_sig = inspect.signature(provider_type)
        if "model_name" in init_sig.parameters:
            if not self.model_name:
                raise EnvironmentError(
                    "Missing model name which is required for this provider; "
                    "please set the 'MODEL_NAME' environment variable or "
                    "instantiate an appropriate LLMClient."
                )
            self._chosen_provider = provider_type(model_name=self.model_name)
        else:
            self._chosen_provider = provider_type()
            self.model_name_in_generate = True

    @classmethod
    def provider_class(cls) -> Type:
        return None

    def _register_methods(self) -> None:
        self._chosen_provider._register_methods()

    def _parse_llm_response(self, raw: Any) -> Union[str, LLMResponse]:
        return self._chosen_provider._parse_llm_response(raw)

    def _setup_parameter_mapper(self) -> None:
        """
        Setup parameter mapping for the provider. Override in subclasses to configure
        mapping from generic GenerationArgs to provider-specific parameters.
        """
        pass

    def generate(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if self.model_name_in_generate:
            # this is needed for providers like openai
            model_name = kwargs.get("model")
            if not model_name:
                model_name = self.model_name
                return self._chosen_provider.generate(*args, model=model_name, **kwargs)
        return self._chosen_provider.generate(*args, **kwargs)

    async def generate_async(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if self.model_name_in_generate:
            # this is needed for providers like openai
            model_name = kwargs.get("model")
            if not model_name:
                model_name = self.model_name
                return await self._chosen_provider.generate_async(
                    *args, model=model_name, **kwargs
                )
        return await self._chosen_provider.generate_async(*args, **kwargs)
