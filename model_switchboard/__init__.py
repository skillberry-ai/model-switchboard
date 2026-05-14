"""Provider-agnostic model generation clients."""

__version__ = "0.1.0"

# Re-export main components from llm module
from .llm import (
    GenerationArgs,
    GenerationMode,
    Hook,
    LLMClient,
    LLMResponse,
    MethodConfig,
    OutputValidationError,
    ValidatingLLMClient,
    get_llm,
    list_available_llms,
    register_llm,
)

# Re-export logging utilities
from .llm.logging_utils import (
    LogConfig,
    configure_logging,
    get_logger,
)

__all__ = [
    "__version__",
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
    "configure_logging",
    "LogConfig",
    "get_logger",
]
