# Model Switchboard

Model Switchboard is a small Python library for calling different model providers through one consistent interface. It supports synchronous and asynchronous generation, tool calls, structured output validation, provider-specific parameter mapping, and configurable logging.

## Installation

```bash
pip install model-switchboard
```

For local development:

```bash
git clone git@github.com:skillberry-ai/model-switchboard.git
cd model-switchboard
pip install -e ".[dev,all]"
```

LiteLLM is installed by default. Additional provider extras are available when you need direct SDK support:

```bash
pip install "model-switchboard[openai]"
pip install "model-switchboard[watsonx]"
pip install "model-switchboard[all]"
```

## Quick Start

```python
from model_switchboard.llm import get_llm

LiteLLMClient = get_llm("litellm")
client = LiteLLMClient(model_name="openai/gpt-4o-mini")

response = client.generate("Write a short explanation of retrieval augmented generation.")
print(response)
```

You can also select a provider from environment variables:

```bash
export LLM_PROVIDER=litellm
export MODEL_NAME=openai/gpt-4o-mini
export OPENAI_API_KEY=...
```

```python
from model_switchboard.llm import get_llm

client = get_llm("auto_from_env")()
print(client.generate("Summarize the role of a model gateway."))
```

If `LLM_PROVIDER` is not set, `auto_from_env` defaults to `litellm`. Providers that need a model name still require `MODEL_NAME`.

## Providers

### LiteLLM

LiteLLM is the default provider and works with any LiteLLM-supported model string.

```python
from model_switchboard.llm import get_llm

client = get_llm("litellm")(model_name="openai/gpt-4o-mini")
response = client.generate(
    [{"role": "user", "content": "Return three release checklist items."}],
    temperature=0.2,
)
```

Registered names:

- `litellm`
- `litellm.output_val`

### OpenAI and Azure OpenAI

Install the direct OpenAI SDK extra when you want to use OpenAI clients without the LiteLLM adapter.

```bash
pip install "model-switchboard[openai]"
```

```python
from model_switchboard.llm import get_llm

client = get_llm("openai.sync")(api_key="...")
response = client.generate("Explain semantic versioning.", model="gpt-4o-mini")
```

Registered names:

- `openai.sync`
- `openai.async`
- `openai.sync.output_val`
- `openai.async.output_val`
- `azure_openai.sync`
- `azure_openai.async`
- `azure_openai.sync.output_val`
- `azure_openai.async.output_val`

### Ollama

Ollama uses the LiteLLM dependency that is installed by default.

```python
from model_switchboard.llm import get_llm

client = get_llm("litellm.ollama")(
    model_name="llama3.1",
    api_base="http://localhost:11434",
)
print(client.generate("Give me one practical use for local models."))
```

Registered names:

- `litellm.ollama`
- `litellm.ollama.output_val`

### Watsonx

Watsonx can be used through LiteLLM or the native SDK.

```bash
pip install "model-switchboard[watsonx]"
```

```python
from model_switchboard.llm import get_llm

client = get_llm("litellm.watsonx")(
    model_name="meta-llama/llama-3-3-70b-instruct",
    api_key="...",
    project_id="...",
)
```

Registered names:

- `litellm.watsonx`
- `litellm.watsonx.output_val`
- `watsonx`
- `watsonx.output_val`

## Structured Output

Use an output-validation provider when you want a Pydantic model, JSON schema, or built-in type back from the response.

```python
from pydantic import BaseModel

from model_switchboard.llm import get_llm


class Task(BaseModel):
    title: str
    priority: str


client = get_llm("litellm.output_val")(model_name="openai/gpt-4o-mini")
task = client.generate(
    "Create one task for preparing a package release.",
    output_schema=Task,
)
print(task.title, task.priority)
```

## Generation Arguments

`GenerationArgs` provides provider-agnostic parameters such as `max_tokens`, `temperature`, `top_p`, `seed`, `timeout`, `stop_sequences`, and `stream`.

```python
from model_switchboard.llm import get_llm
from model_switchboard.llm.types import GenerationArgs

client = get_llm("litellm")(model_name="openai/gpt-4o-mini")
args = GenerationArgs(max_tokens=120, temperature=0.3, seed=7)

response = client.generate("Draft a concise changelog entry.", generation_args=args)
```

Each provider maps supported arguments to its native SDK shape and ignores unsupported values with a warning where appropriate.

## Logging

```python
from model_switchboard import configure_logging

configure_logging(level="INFO")
```

Environment variables:

- `MODEL_SWITCHBOARD_LOG_LEVEL`
- `MODEL_SWITCHBOARD_LOG_DIR`

Sensitive keys such as API keys, tokens, credentials, and authorization headers are masked before logging.

## Examples

Example scripts live in `llm_examples/`:

- `litellm_ollama_example.py`
- `azure_openai_example.py`
- `litellm_watsonx_example.py`
- `ibm_watsonx_ai_example.py`
- `litellm_rits_example.py`
- `litellm_ibm_example.py`

Run an example from the repository root:

```bash
python llm_examples/litellm_ollama_example.py
```

## Enterprise/Internal Integrations

RITS and IBM ETE LiteLLM adapters are included for internal IBM services.

RITS:

- Provider names: `litellm.rits`, `litellm.rits.output_val`
- Environment variables: `RITS_API_KEY`, `RITS_API_URL`

IBM ETE LiteLLM:

- Provider names: `litellm.ibm`, `litellm.ibm.output_val`
- Environment variables: `IBM_THIRD_PARTY_API_KEY`, `IBM_LITELLM_API_BASE`

## Development

```bash
pip install -e ".[dev,all]"
make lint
make coverage
make build
```

Release builds are created with:

```bash
python -m build
twine check dist/*
```

## License

Apache-2.0
