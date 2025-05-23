# Pydantic AI tool integration

## Overview

Pydantic AI tool integration refers to the process of wrapping, validating, and interoperating external tools (such as APIs, functions, or command-line utilities) using [Pydantic](https://docs.pydantic.dev/), a robust data validation and settings management library in Python. In the context of modern AI systems and agent frameworks—such as AG2—this integration enables seamless, type-safe invocation of heterogeneous tools, facilitating dependency injection, automated documentation, and smooth interoperability across different tool ecosystems.

## Explanation

### Why Integrate Tools with Pydantic?

- **Type Safety:** Pydantic models provide strong typing and validation for tool input/output.
- **Interoperability:** Standardizing tool interfaces enables composition and orchestration across frameworks and languages.
- **Automation:** AG2 and similar frameworks can auto-generate UI, docs, and client code from Pydantic models.
- **Dependency Injection:** Inputs and dependencies can be injected automatically, simplifying complex workflows.

### AG2 Tool Format

AG2 (AgentGPT Generation 2) defines a standardized format for tools:
- **Input/Output Schemas:** Defined using Pydantic models.
- **Metadata:** Includes tool name, description, and usage.
- **Execution Method:** A standard method to invoke the tool (e.g., `run`).

### Converting External Tools

To integrate an external tool:
1. **Define Pydantic Models:** Map the tool's input and output to Pydantic models.
2. **Wrap Execution Logic:** Implement a class/method that validates inputs, calls the tool, and returns outputs as Pydantic models.
3. **Register Tool:** Use AG2 or your agent framework's registration system for discovery and orchestration.

### Interoperability Classes

Interoperability classes encapsulate logic to:
- Handle multiple tool formats (local, API, CLI, etc.)
- Validate and coerce types between ecosystems
- Bridge between AG2 Tool format and external systems

## Examples

### 1. Wrapping an External Function

Suppose you have a simple weather API function:

```python
def get_weather(city: str, units: str = "metric") -> dict:
    # Calls external API...
    return {"temperature": 22.5, "units": units}
```

#### Step 1: Define Pydantic Schemas

```python
from pydantic import BaseModel

class WeatherInput(BaseModel):
    city: str
    units: str = "metric"

class WeatherOutput(BaseModel):
    temperature: float
    units: str
```

#### Step 2: Create AG2 Tool Wrapper

```python
class GetWeatherTool:
    name = "get_weather"
    description = "Get current temperature in a city."
    input_model = WeatherInput
    output_model = WeatherOutput

    def run(self, input: WeatherInput) -> WeatherOutput:
        result = get_weather(input.city, input.units)
        return WeatherOutput(**result)
```

#### Step 3: Register Tool

```python
from ag2.tools import register_tool

register_tool(GetWeatherTool())
```

### 2. Interoperability Class Example

For a CLI tool (e.g., `curl`):

```python
class CurlInput(BaseModel):
    url: str

class CurlOutput(BaseModel):
    response: str

class CurlTool:
    name = "curl"
    description = "Fetches content from a URL."
    input_model = CurlInput
    output_model = CurlOutput

    def run(self, input: CurlInput) -> CurlOutput:
        import subprocess
        result = subprocess.run(['curl', input.url], capture_output=True, text=True)
        return CurlOutput(response=result.stdout)
```

## Best Practices

- **Always use explicit Pydantic models** for input and output—even if your tool has a simple signature. This ensures consistent validation and documentation.
- **Handle errors gracefully** in your wrapper classes, raising descriptive exceptions for invalid inputs or failed executions.
- **Use dependency injection** for shared resources (like HTTP clients or database connections) rather than hardcoding them.
- **Document tool metadata** (name, description, usage) to improve discoverability and auto-generated docs.
- **Test your wrappers** with a variety of inputs and edge cases to ensure robust validation.
- **Keep interoperability layers thin**—avoid complex business logic in the wrapper itself.

## Common Pitfalls

- **Forgetting to validate outputs**: Always ensure returned data matches the output schema.
- **Leaking tool-specific exceptions**: Catch and re-raise as standard errors for the agent framework.
- **Omitting default values** in schemas, leading to unnecessary validation failures.
- **Tight coupling**: Avoid hardwiring tool-specific logic into the agent; keep wrappers generic.

## Related Concepts

- [Tools and Dependency Injection](./tools-and-dependency-injection.md)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [AG2 Tool Format](https://github.com/agentgpt/AG2)
- [Function and Tool Orchestration](./function-and-tool-orchestration.md)
- [Type-Safe AI Agents](./type-safe-ai-agents.md)
- [Error Handling with Pydantic](https://docs.pydantic.dev/usage/validation_decorator/)
- [OpenAPI & Pydantic](https://fastapi.tiangolo.com/tutorial/body/)

---

By following these guidelines, you can efficiently convert and integrate external tools into interoperable, robust AI agent workflows using Pydantic and AG2 or similar frameworks.