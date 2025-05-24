# Config list and filtering

## Overview

When working with Large Language Models (LLMs) in modern ML applications, it's common to support multiple backends (e.g., OpenAI, Azure, HuggingFace, local models). To manage these, you use **LLM configuration objects (LLMConfig)** and organize them into **config lists**. Filtering allows you to select, validate, and manage which models or model clients are active based on your requirements or runtime conditions. This enables dynamic backend support, simplifies dependency injection, and makes multi-model orchestration robust and maintainable.

---

## Explanation

### LLMConfig and Config Lists

- **LLMConfig**: A structured object or class encapsulating the settings needed to instantiate and operate an LLM. This might include model name, API keys, endpoint URLs, and backend type.
- **Config List**: An iterable collection (list, tuple, etc.) of LLMConfig instances. This allows you to enumerate all available LLMs, regardless of their backend.

Example:
```python
class LLMConfig:
    def __init__(self, name, backend, api_key=None, endpoint=None):
        self.name = name
        self.backend = backend
        self.api_key = api_key
        self.endpoint = endpoint
```

```python
config_list = [
    LLMConfig(name="gpt-3.5-turbo", backend="openai", api_key="sk-..."),
    LLMConfig(name="llama-2-7b", backend="huggingface", endpoint="http://localhost:8000"),
    LLMConfig(name="azure-gpt4", backend="azure", api_key="az-...", endpoint="https://azure.openai.com/"),
]
```

### Filtering Config Lists

Filtering refers to selecting configurations that match certain criteria (e.g., backend type, model name, or feature support). This is essential for:

- **Dependency injection**: Providing only the relevant model to a component.
- **Multi-backend support**: Choosing the best available backend at runtime.
- **Validation**: Ensuring only valid/working configs are used.

#### Filtering Example

```python
def filter_configs(config_list, backend=None, name=None):
    return [
        config for config in config_list
        if (backend is None or config.backend == backend)
        and (name is None or config.name == name)
    ]

# Filter for OpenAI models
openai_configs = filter_configs(config_list, backend="openai")
```

### Model Client Selection and Validation

Once filtered, configs are instantiated as model clients. Validation may include checking API connectivity, credentials, or supported features.

```python
def validate_config(config):
    # Simple validation example
    if config.backend == "openai" and not config.api_key:
        raise ValueError(f"Missing API key for {config.name}")
    # Add backend-specific checks...
    return True

valid_configs = [c for c in openai_configs if validate_config(c)]
```

---

## Examples

### Example 1: Basic Config List and Filtering

```python
config_list = [
    LLMConfig("gpt-4", "openai", api_key="..."),
    LLMConfig("llama-13b", "huggingface", endpoint="http://localhost:8000"),
    LLMConfig("gpt-35", "azure", api_key="...", endpoint="https://az.openai.com"),
]

# Get only HuggingFace configs
hf_configs = filter_configs(config_list, backend="huggingface")
for cfg in hf_configs:
    print(cfg.name)  # Output: llama-13b
```

### Example 2: Dependency Injection for a Service

```python
class SummarizerService:
    def __init__(self, llm_client):
        self.llm_client = llm_client

# Select and validate an OpenAI client
openai_config = filter_configs(config_list, backend="openai")[0]
validate_config(openai_config)
summarizer = SummarizerService(llm_client=openai_config)
```

### Example 3: Dynamic Multi-Backend Orchestration

```python
def get_best_available_llm(config_list):
    # Prioritize OpenAI, fallback to others
    for backend in ["openai", "azure", "huggingface"]:
        candidates = filter_configs(config_list, backend=backend)
        for config in candidates:
            try:
                validate_config(config)
                return config
            except Exception:
                continue
    raise RuntimeError("No valid LLM configuration available.")

llm_config = get_best_available_llm(config_list)
```

---

## Best Practices

- **Centralize Configuration**: Keep all LLM settings in one place for easier management.
- **Use Filtering Functions**: Always filter configs based on backend, model, or feature needs.
- **Validate Early**: Validate configs before using them to avoid runtime failures.
- **Abstract Model Clients**: Interact with LLMs via client classes that wrap configs for dependency injection.
- **Support Fallbacks**: Always consider fallback strategies for multi-backend robustness.
- **Document Config Structure**: Clearly document what each config field means and which are required for each backend.

**Common Pitfalls:**
- Not validating API keys or endpoints before use.
- Hardcoding selection logic instead of using flexible filters.
- Mixing config and client instantiation logic, leading to tight coupling.

---

## Related Concepts

- [LLMConfig and LLMConfigEntry](llmconfig-and-llmconfigentry.html)
- [Model Client Protocol](modelclient-protocol.html)
- [Multi-Backend LLM Orchestration](multi-backend-llm.html)
- [Prompt Engineering](prompt-engineering.html)
- [Tools and Dependency Injection](tools-dependency-injection.html)

For further reading:
- [Dependency Injection Patterns in Python](https://realpython.com/dependency-injection-python/)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/best-practices)
- [HuggingFace Transformers Documentation](https://huggingface.co/docs/transformers/index)

---

*This documentation outlines how to use config lists and filtering to enable robust, scalable, and maintainable LLM integration across multiple backends.*