# LLMConfig and LLMConfigEntry

## Overview

`LLMConfig` and `LLMConfigEntry` provide a standardized way to configure and manage Language Model (LLM) backends in modern machine learning and AI applications. These abstractions enable developers to flexibly define, select, and validate different LLMs, whether running locally or via cloud APIs, while supporting dependency injection and multi-backend switching. This configuration layer is essential for scalable, maintainable, and testable AI systems.

---

## Explanation

### What are LLMConfig and LLMConfigEntry?

- **LLMConfigEntry**: Represents a single LLM configuration, encapsulating parameters such as model name, backend type, API keys, endpoints, and other settings.
- **LLMConfig**: A collection (often a list or registry) of multiple `LLMConfigEntry` objects, enabling support for multiple models or backends within the same application.

These constructs allow applications to:

- Define multiple LLM backends (e.g., OpenAI, HuggingFace, Azure, local models).
- Filter/select the most appropriate model client based on use-case.
- Validate configuration correctness at startup or runtime.
- Inject model clients using dependency injection patterns.

### How Does It Work?

1. **Configuration Definition**: 
   - Each backend/model is described via an `LLMConfigEntry`.
   - Entries are collected into an `LLMConfig` list.
2. **Selection & Filtering**: 
   - At runtime, code selects the appropriate config entry based on tags, backend type, or other metadata.
3. **Validation**: 
   - Each entry can be validated for required fields (e.g., API keys).
4. **Dependency Injection**: 
   - Tools and frameworks inject configured clients into business logic, decoupling model selection from usage.

### Example LLMConfigEntry Fields

| Field          | Description                          | Example Value                |
|----------------|--------------------------------------|------------------------------|
| `name`         | Human-readable name                  | "OpenAI GPT-4"               |
| `backend`      | Backend identifier                   | "openai", "huggingface"      |
| `model`        | Model name or ID                     | "gpt-4", "llama-2-70b"       |
| `api_key`      | API key or credential (if needed)    | "sk-..."                     |
| `endpoint`     | Custom endpoint URL                  | "https://api.openai.com/"    |
| `tags`         | Custom tags for filtering            | ["prod", "fast"]             |
| `params`       | Additional backend/model parameters  | `{"temperature": 0.7}`       |

---

## Examples

### 1. Defining LLMConfigEntry and LLMConfig

```python
# Example structure (Python)

from typing import List, Dict, Optional

class LLMConfigEntry:
    def __init__(
        self,
        name: str,
        backend: str,
        model: str,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        tags: Optional[List[str]] = None,
        params: Optional[Dict] = None
    ):
        self.name = name
        self.backend = backend
        self.model = model
        self.api_key = api_key
        self.endpoint = endpoint
        self.tags = tags or []
        self.params = params or {}

# Collection of configs
LLMConfig = List[LLMConfigEntry]
```

### 2. Sample Configuration List

```python
llm_config: LLMConfig = [
    LLMConfigEntry(
        name="OpenAI GPT-4",
        backend="openai",
        model="gpt-4",
        api_key="sk-...",
        tags=["prod", "default"]
    ),
    LLMConfigEntry(
        name="HuggingFace Llama 2",
        backend="huggingface",
        model="llama-2-70b",
        api_key="hf_...",
        endpoint="https://api-inference.huggingface.co/models/llama-2-70b",
        tags=["experimental"]
    ),
    LLMConfigEntry(
        name="Local GPT4All",
        backend="gpt4all",
        model="gpt4all-j",
        tags=["local", "offline"]
    )
]
```

### 3. Selecting and Validating a Model Client

```python
def select_llm(config: LLMConfig, tag: str) -> LLMConfigEntry:
    for entry in config:
        if tag in entry.tags:
            validate_llm_entry(entry)
            return entry
    raise ValueError(f"No LLM with tag '{tag}' found.")

def validate_llm_entry(entry: LLMConfigEntry):
    if entry.backend in ["openai", "huggingface"] and not entry.api_key:
        raise ValueError(f"{entry.backend} backend requires an API key.")

# Usage
chosen_entry = select_llm(llm_config, "prod")
print(f"Selected model: {chosen_entry.name} ({chosen_entry.model})")
```

### 4. Dependency Injection Example (with FastAPI)

```python
from fastapi import Depends, FastAPI

def get_llm_entry() -> LLMConfigEntry:
    # For demonstration, always select 'prod'
    return select_llm(llm_config, "prod")

app = FastAPI()

@app.post("/generate")
def generate(prompt: str, llm_entry: LLMConfigEntry = Depends(get_llm_entry)):
    # Use llm_entry to instantiate and call the model client
    ...
```

---

## Best Practices

- **Centralize Configuration**: Keep all `LLMConfigEntry` instances in a central location (e.g., config file, environment module).
- **Secure Secrets**: Never hard-code API keys; use environment variables or secret managers.
- **Use Tags and Metadata**: Tag entries for easy selection (e.g., `["prod"]`, `["test"]`, `["fast"]`).
- **Validate Early**: Validate configuration at startup to catch missing fields or invalid values.
- **Support Overrides**: Allow environment or runtime overrides (e.g., via CLI or ENV) for model selection.
- **Separate Concerns**: Keep configuration and client logic separate for testability and clarity.
- **Document Each Entry**: Add comments or documentation for each config entry to explain its purpose.
- **Handle Multi-Backend**: Ensure your code can handle different backends' requirements and parameters.
- **Monitor and Rotate Keys**: Regularly audit and rotate API keys used in configs.

---

## Related Concepts

- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- [Model Client Abstraction](model-client-abstraction.md)
- [Multi-Backend LLM Orchestration](multi-backend-llm.md)
- [Configuration Management in Python](https://docs.python.org/3/library/configparser.html)
- [Environment Variables and Secret Management](https://12factor.net/config)
- [Prompt Engineering](prompt-engineering.md)
- [LLM Client Libraries (e.g., OpenAI, HuggingFace Transformers)](https://platform.openai.com/docs/libraries)

---

**See also:**  
- [Tools and Dependency Injection](tools-dependency-injection.md)  
- [Filtering and Routing Requests to LLMs](llm-routing.md)