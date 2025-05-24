# Interoperability registry

## Overview

The **Interoperability registry** is a core design pattern in AG2 (Agent Generation 2) that enables the seamless integration of external tools, libraries, and functions into the AG2 tool ecosystem. By registering interoperability classes, developers can convert tools from diverse programming languages and frameworks into AG2-compliant tools, making them discoverable and usable across agent workflows. This registry acts as a bridge, allowing dependency-injected tools and functions to communicate and interoperate efficiently, facilitating multi-ecosystem integration.

---

## Explanation

The interoperability registry is a centralized component that stores mappings between external tool definitions and their AG2 Tool format equivalents. This mechanism allows agents to:

- **Discover** external tools at runtime.
- **Inject dependencies** using AG2's dependency injection system.
- **Invoke and orchestrate** tools, regardless of their origin (e.g., Python, JavaScript, REST APIs).

### Key Steps

1. **Conversion:** External tools (e.g., Python modules, Node packages, REST endpoints) are wrapped or adapted into AG2 Tool format via interoperability classes.
2. **Registration:** These interoperability classes are registered with the registry, making them available to AG2 agents.
3. **Usage:** Agents query the registry to discover and use registered tools in workflows.

**Interoperability classes** serve as adapters or bridges, encapsulating the conversion logic and tool-specific metadata. The registry ensures that once a tool is registered, it can be reused by any agent or component within the system.

---

## Examples

### Example 1: Converting a Python Library Function

Suppose you have a Python function from an external library that you want to expose as an AG2 tool:

```python
# external_tool.py
def summarize(text: str) -> str:
    return text[:50] + '...'
```

#### Step 1: Create an Interoperability Class

```python
# ag2_interop.py
from ag2.interop import InteroperabilityRegistry, ToolAdapter

class SummarizeAdapter(ToolAdapter):
    tool_name = "summarize"

    def run(self, text: str) -> str:
        from external_tool import summarize
        return summarize(text)

# Register the adapter
InteroperabilityRegistry.register(SummarizeAdapter)
```

#### Step 2: Use the Registered Tool

```python
from ag2.interop import InteroperabilityRegistry

summarize_tool = InteroperabilityRegistry.get("summarize")
result = summarize_tool.run("This is a long piece of text that needs summarization.")
print(result)  # Output: This is a long piece of text that needs summar...
```

---

### Example 2: Integrating a REST API

```python
import requests
from ag2.interop import InteroperabilityRegistry, ToolAdapter

class WeatherAPIAdapter(ToolAdapter):
    tool_name = "get_weather"

    def run(self, location: str) -> dict:
        response = requests.get(f"https://api.weather.com/v3/weather/{location}")
        return response.json()

InteroperabilityRegistry.register(WeatherAPIAdapter)
```

---

### Example 3: Dependency Injection

If your tool requires dependencies, AG2's DI system can inject them:

```python
from ag2.di import inject

class DatabaseAdapter(ToolAdapter):
    tool_name = "db_query"

    @inject
    def __init__(self, db_client):
        self.db_client = db_client

    def run(self, query: str):
        return self.db_client.execute(query)

InteroperabilityRegistry.register(DatabaseAdapter)
```

---

## Best Practices

- **Encapsulation:** Always encapsulate external tool logic within dedicated interoperability classes (adapters).
- **Clear Metadata:** Define tool names and descriptions clearly for discoverability.
- **Type Safety:** Use explicit type annotations for input/output.
- **Error Handling:** Handle exceptions gracefully within adapters to prevent agent failures.
- **Avoid Side Effects:** Ensure adapters do not introduce unexpected side effects.
- **Reusability:** Register adapters once for global reuse.
- **Documentation:** Document each adapter’s purpose, required dependencies, and usage.

**Common Pitfalls:**

- Registering duplicate tool names (causes conflicts)
- Failing to handle external tool errors, leading to agent crashes
- Hardcoding dependencies instead of using dependency injection
- Not updating the registry after changing adapter logic

---

## Related Concepts

- [Tools and Dependency Injection](./tools_dependency_injection.md)
- [AG2 Tool Format](./ag2_tool_format.md)
- [Function Wrapping and Conversion](./function_wrapping.md)
- [Agent Workflow Composition](./agent_workflow.md)
- [Dependency Injection in AG2](./di_in_ag2.md)
- [External API Integration](./external_api_integration.md)

For more details, see the [AG2 documentation](https://ag2-docs.example.com/interoperability).