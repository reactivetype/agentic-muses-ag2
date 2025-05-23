# Interoperable protocol

## Overview

The **Interoperable protocol** defines a standard method for integrating and orchestrating tools and functions from multiple ecosystems (such as Python libraries, REST APIs, or external services) within a single, unified environment. By adhering to this protocol, developers can convert external tools into a common format (such as the AG2 Tool format), register them as interoperable classes, and seamlessly use them alongside native functions. This enables dependency injection, reusability, and modularity across diverse technology stacks.

---

## Explanation

In complex applications, you often need to leverage tools that originate from different ecosystems—such as a Python library, a Node.js module, or an HTTP API. The Interoperable protocol provides a structured way to:

- **Wrap external tools** so they adhere to a common interface.
- **Register these tools as classes** that can be discovered and injected where needed.
- **Invoke these tools/functions** as if they were native, regardless of their source.

### AG2 Tool Format

The AG2 Tool format is an abstraction that standardizes the interface for tools. A tool is typically represented as a class or function with a defined input/output schema, metadata, and lifecycle hooks.

### Interoperability Classes

An interoperability class wraps an external tool or function, adapting its interface to the AG2 Tool format. This allows for dependency injection, orchestrated execution, and type-safe integration.

### Multiecosystem Integration

By using the Interoperable protocol, you can mix-and-match tools from different sources, e.g., call a Python function, a JavaScript module, and a REST API within a single workflow.

---

## Examples

### 1. Converting an External Tool to AG2 Tool Format

Suppose you have an external function `calculate_tax`:

```python
# External tool
def calculate_tax(amount: float, rate: float) -> float:
    return amount * rate
```

Wrap it in the AG2 Tool format:

```python
from ag2.interop import Tool

class CalculateTaxTool(Tool):
    name = "calculate_tax"
    description = "Calculates tax given an amount and rate."
    input_schema = {"amount": float, "rate": float}
    output_schema = float

    def run(self, amount: float, rate: float) -> float:
        return calculate_tax(amount, rate)
```

### 2. Registering an Interoperability Class

```python
from ag2.registry import register_tool

register_tool(CalculateTaxTool)
```

Now the tool can be injected and used whenever needed.

### 3. Integrating Tools from Multiple Ecosystems

Suppose you have:

- A Python function (`calculate_tax`)
- A REST API for currency conversion

Wrap the API as a tool:

```python
import requests
from ag2.interop import Tool

class CurrencyConversionTool(Tool):
    name = "convert_currency"
    description = "Converts currency using an external API."
    input_schema = {"amount": float, "from_currency": str, "to_currency": str}
    output_schema = float

    def run(self, amount, from_currency, to_currency):
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/" + from_currency
        )
        rate = response.json()["rates"][to_currency]
        return amount * rate
```

Register and use both tools in a workflow:

```python
from ag2.interop import inject

@inject
def process_invoice(amount: float, from_currency: str, to_currency: str, 
                    calculate_tax: CalculateTaxTool, 
                    convert_currency: CurrencyConversionTool):
    taxed = calculate_tax.run(amount, rate=0.07)
    converted = convert_currency.run(taxed, from_currency, to_currency)
    return converted
```

---

## Best Practices

- **Standardize Interfaces:** Ensure all tools conform to the AG2 Tool format (input/output schemas, metadata).
- **Encapsulate External Logic:** Use interoperability classes to isolate third-party dependencies.
- **Leverage Dependency Injection:** Register your tools so they can be injected wherever needed.
- **Error Handling:** Validate inputs and handle errors gracefully within interoperability wrappers.
- **Document Tools:** Clearly document each tool's purpose, inputs, and outputs for maintainability.
- **Test Integration Points:** Write integration tests to confirm tools from different ecosystems work together as expected.
- **Limit Surface Area:** Only expose necessary functionality through the interoperable interface.

**Common Pitfalls:**

- Forgetting to register a tool, making it unavailable for injection.
- Not handling API failures or network errors in external integrations.
- Overcomplicating the interface; keep your interoperability classes focused and minimal.

---

## Related Concepts

- [Tools and Dependency Injection](./tools-and-dependency-injection.md)
- [AG2 Tool Format](./ag2-tool-format.md)
- [Service Registration and Discovery](./service-registration-discovery.md)
- [Orchestrating Multiecosystem Workflows](./multi-ecosystem-workflows.md)
- [Error Handling in Interoperable Systems](./error-handling-interoperable-systems.md)

For further reading, see:
- [Design Patterns: Adapter Pattern](https://refactoring.guru/design-patterns/adapter)
- [Python Dependency Injection](https://docs.python.org/3/glossary.html#term-dependency-injection)

---