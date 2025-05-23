# ModelClient protocol

## Overview

The **ModelClient protocol** defines a standard interface for interacting with different Large Language Model (LLM) backends within a configurable and extensible system. By abstracting the details of each LLM provider (OpenAI, Azure, local models, etc.), the `ModelClient` protocol enables seamless model selection, validation, and invocation across multiple backends. This protocol is essential when building applications that require flexibility in switching or combining LLM providers for tasks such as text generation, chat, or embeddings.

## Explanation

The `ModelClient` protocol typically specifies a set of methods and properties that all LLM client implementations must follow. This abstraction allows you to:

- **Configure LLMs** using objects like `LLMConfig` and configuration lists.
- **Select and validate** which backend or model client to use based on runtime context or application needs.
- **Filter and manage** multiple configurations, enabling multi-backend support (e.g., failover, routing, or A/B testing).

### Key Components

1. **LLMConfig:**  
   A configuration object that holds model parameters (model name, API key, base URL, etc.) relevant to a specific backend.

2. **ModelClient (Protocol/Base Class):**  
   An interface that defines methods such as `generate`, `validate`, and `get_config`.

3. **Dependency Injection:**  
   Model clients are often instantiated via dependency injection, allowing for flexible swapping and testing.

4. **Config Lists:**  
   Collections of `LLMConfig` objects, enabling dynamic selection and management of available models.

### Typical Protocol Methods

```python
from typing import Protocol, Any, Dict

class ModelClient(Protocol):
    def generate(self, prompt: str, config: 'LLMConfig') -> str:
        """Generate text based on the prompt and configuration."""
        ...

    def validate(self, config: 'LLMConfig') -> bool:
        """Check if the configuration is valid for this client."""
        ...

    def get_config(self) -> 'LLMConfig':
        """Return the current LLM configuration."""
        ...
```

This allows consumers to use any compliant model client interchangeably within the application.

## Examples

### 1. Defining an LLMConfig

```python
class LLMConfig:
    def __init__(self, model_name: str, api_key: str, base_url: str = None, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.extra_params = kwargs
```

### 2. Implementing a ModelClient for OpenAI

```python
class OpenAIClient:
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str, config: LLMConfig = None) -> str:
        # Imagine this calls OpenAI's API
        config = config or self.config
        # ... (actual API logic here)
        return f"OpenAI response to: {prompt}"

    def validate(self, config: LLMConfig = None) -> bool:
        config = config or self.config
        return config.api_key is not None and config.model_name.startswith("gpt-")

    def get_config(self) -> LLMConfig:
        return self.config
```

### 3. Selecting and Validating Model Clients from a Config List

```python
config_list = [
    LLMConfig(model_name="gpt-4", api_key="openai-key"),
    LLMConfig(model_name="llama-2", api_key="local-key", base_url="http://localhost:8000"),
]

clients = [OpenAIClient(cfg) for cfg in config_list if cfg.model_name.startswith("gpt-")]

# Validate and select a client
valid_clients = [client for client in clients if client.validate()]
selected_client = valid_clients[0]
response = selected_client.generate("Hello, world!")
print(response)
```

## Best Practices

- **Abstract with Protocols:** Always use protocols or base classes to define model clients instead of relying on concrete implementations.
- **Centralize Configuration:** Store and manage LLM configurations in a central location for easier maintenance and updates.
- **Use Dependency Injection:** Inject model clients where needed to improve testability and flexibility.
- **Validate Before Use:** Always validate configurations before invoking a model client to prevent runtime errors.
- **Support Multi-Backend Strategies:** Design your system to easily switch, combine, or fallback between different LLM providers.
- **Handle Errors Gracefully:** Implement error handling for failed validation, API errors, or misconfigurations.
- **Document Config Fields:** Clearly document which configuration fields are required by each model client.

## Related Concepts

- [LLMConfig](#) - Model configuration objects for LLM clients.
- [Dependency Injection](#) - Patterns for injecting dependencies like model clients.
- [Config Lists](#) - Managing multiple LLM configurations for multi-backend support.
- [LLM Selection and Routing](#) - Strategies for routing requests to different model backends.
- [Provider Abstraction Patterns](#) - Techniques for abstracting third-party services.

---

For further reading, see:
- [PEP 544 – Protocols: Structural subtyping (static duck typing)](https://peps.python.org/pep-0544/)
- [Dependency Injection in Python](https://realpython.com/dependency-injection-python/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction)