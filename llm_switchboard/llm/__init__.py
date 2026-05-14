"""Core registry, types, and provider imports for LLM Switchboard."""

from typing import Dict, Type

# Global registry for provider clients - initialize once.
_REGISTRY: Dict[str, Type["LLMClient"]] = {}

# Core imports
from .base import (
    Hook,
    LLMClient,
    MethodConfig,
    get_llm,
    list_available_llms,
    register_llm,
)
from .output_parser import OutputValidationError, ValidatingLLMClient
from .types import GenerationArgs, GenerationMode, LLMResponse

# Export core components
__all__ = [
    "LLMClient",
    "ValidatingLLMClient",
    "get_llm",
    "register_llm",
    "list_available_llms",
    "Hook",
    "MethodConfig",
    "OutputValidationError",
    "GenerationMode",
    "LLMResponse",
    "GenerationArgs",
]


# Conditional imports for providers
def _import_providers():
    """Import providers with optional dependencies."""

    from .providers.auto_from_env.auto_from_env import AutoFromEnvLLMClient

    __all__.extend(["AutoFromEnvLLMClient"])

    # LiteLLM providers
    try:
        from .providers.litellm.ibm_litellm import (
            IBMLiteLLMClient,
            IBMLiteLLMClientOutputVal,
        )
        from .providers.litellm.litellm import LiteLLMClient, LiteLLMClientOutputVal
        from .providers.litellm.ollama import (
            OllamaLiteLLMClient,
            OllamaLiteLLMClientOutputVal,
        )
        from .providers.litellm.rits import (
            RITSLiteLLMClient,
            RITSLiteLLMClientOutputVal,
        )
        from .providers.litellm.watsonx import (
            WatsonxLiteLLMClient,
            WatsonxLiteLLMClientOutputVal,
        )

        __all__.extend(
            [
                "LiteLLMClient",
                "LiteLLMClientOutputVal",
                "RITSLiteLLMClient",
                "RITSLiteLLMClientOutputVal",
                "OllamaLiteLLMClient",
                "OllamaLiteLLMClientOutputVal",
                "WatsonxLiteLLMClient",
                "WatsonxLiteLLMClientOutputVal",
                "IBMLiteLLMClient",
                "IBMLiteLLMClientOutputVal",
            ]
        )

    except ImportError:
        pass

    # OpenAI providers
    try:
        from .providers.openai.openai import (
            AsyncAzureOpenAIClient,
            AsyncAzureOpenAIClientOutputVal,
            AsyncOpenAIClient,
            AsyncOpenAIClientOutputVal,
            SyncAzureOpenAIClient,
            SyncAzureOpenAIClientOutputVal,
            SyncOpenAIClient,
            SyncOpenAIClientOutputVal,
        )

        __all__.extend(
            [
                "SyncOpenAIClient",
                "AsyncOpenAIClient",
                "SyncOpenAIClientOutputVal",
                "AsyncOpenAIClientOutputVal",
                "SyncAzureOpenAIClient",
                "AsyncAzureOpenAIClient",
                "SyncAzureOpenAIClientOutputVal",
                "AsyncAzureOpenAIClientOutputVal",
            ]
        )

    except ImportError:
        pass

    # Watsonx providers
    try:
        from .providers.ibm_watsonx_ai.ibm_watsonx_ai import (
            WatsonxLLMClient,
            WatsonxLLMClientOutputVal,
        )

        __all__.extend(["WatsonxLLMClient", "WatsonxLLMClientOutputVal"])

    except ImportError:
        pass


# Initialize providers on import
_import_providers()
