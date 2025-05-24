# LangChain and CrewAI Tool Conversion

## Overview

Modern AI agent frameworks such as **LangChain** and **CrewAI** provide powerful abstractions for building LLM-powered applications. However, these frameworks often define their own tool and function interfaces, which can make interoperability and code reuse challenging. Tool conversion enables you to **adapt tools and functions from one ecosystem (e.g., LangChain) to another (e.g., CrewAI or AG2)**, allowing you to build composite agents and pipelines that leverage the strengths of multiple libraries.

This chapter explains how to convert external tools to a standard format (such as AG2 Tool), register and use interoperability layers, and integrate tools and functions across frameworks using dependency injection.

---

## Explanation

### What is Tool Conversion?

Tool conversion is the process of **adapting a function or tool** (for example, a LangChain Tool or CrewAI Tool) to a standard interface so it can be used interchangeably in other agent frameworks. This often involves:

- **Wrapping**: Encapsulating a tool in an adapter class.
- **Dependency Injection**: Passing dependencies (like API clients) to tools at runtime.
- **Format Standardization**: Ensuring input/output signatures match expectations.

### Why is this Important?

- **Reuse**: Leverage existing tools across frameworks, avoiding duplication.
- **Composability**: Build complex agents that orchestrate capabilities from multiple ecosystems.
- **Maintainability**: Standard interfaces make code easier to manage and extend.

### How Does It Work?

1. **Identify the External Tool**: Locate a tool or function you want to reuse (e.g., a LangChain tool).
2. **Wrap or Convert**: Use an interoperability class or adapter to conform the tool to the target interface (e.g., AG2 Tool).
3. **Register**: Register the converted tool within your agent or tool registry.
4. **Inject Dependencies**: Provide any required resources (like database connections) using dependency injection.

#### AG2 Tool Format

A typical AG2 Tool interface might look like this (in Python):

```python
class AG2Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
```

#### Interoperability Classes

These are adapter classes designed to bridge tool interfaces. For example, you might have:

- `LangChainToolAdapter`
- `CrewAIToolAdapter`

---

## Examples

### 1. Converting a LangChain Tool to AG2 Tool

Suppose you have a LangChain tool:

```python
from langchain.tools import Tool

def search_api(query: str) -> str:
    # Implementation here
    return "search results"

langchain_tool = Tool(
    name="search",
    func=search_api,
    description="Searches the web for information."
)
```

**Adapter for AG2 Tool:**

```python
class LangChainToolAdapter:
    def __init__(self, lc_tool):
        self.name = lc_tool.name
        self.description = lc_tool.description
        self.func = lc_tool.func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

# Convert the tool
ag2_tool = LangChainToolAdapter(langchain_tool)
```

Now `ag2_tool` can be registered in an AG2 agent.

---

### 2. Registering and Using Interoperability Classes

Suppose your agent framework expects tools to be registered in a registry:

```python
tool_registry = {}

def register_tool(tool):
    tool_registry[tool.name] = tool

register_tool(ag2_tool)
```

Now, the agent can use `tool_registry["search"]("LangChain and CrewAI interoperability")`.

---

### 3. Integrating CrewAI Tool

Suppose you have a CrewAI tool:

```python
class CrewAITool:
    def __init__(self, name, execute_fn):
        self.name = name
        self.execute = execute_fn

    def execute(self, *args, **kwargs):
        # Tool logic
        pass

crew_tool = CrewAITool("summarizer", lambda text: text[:100])
```

**Adapter Example:**

```python
class CrewAIToolAdapter:
    def __init__(self, crew_tool):
        self.name = crew_tool.name
        self.description = getattr(crew_tool, 'description', '')
        self.func = crew_tool.execute

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

ag2_tool_crew = CrewAIToolAdapter(crew_tool)
register_tool(ag2_tool_crew)
```

---

### 4. Dependency Injection Example

If your tool needs an API client:

```python
class SearchTool:
    def __init__(self, api_client):
        self.api_client = api_client

    def __call__(self, query):
        return self.api_client.search(query)

# Inject the dependency at registration time
api_client = MySearchApiClient()
search_tool = SearchTool(api_client)
register_tool(search_tool)
```

---

## Best Practices

- **Use Adapter Classes**: Always encapsulate external tools with adapters to maintain decoupling.
- **Maintain Clear Interfaces**: Standardize input/output signatures for all tools.
- **Document Dependencies**: Clearly specify any required dependencies for each tool.
- **Test Conversions**: Validate that converted tools behave as expected in the new ecosystem.
- **Leverage Dependency Injection**: Avoid hard-coding dependencies inside tool code.
- **Handle Errors Gracefully**: Ensure adapters catch and re-raise or log exceptions meaningfully.

### Common Pitfalls

- **Mismatched Signatures**: Not adapting argument lists can lead to runtime errors.
- **Stateful Tools**: Some tools maintain internal state; ensure adapters handle this appropriately.
- **Unregistered Tools**: Forgetting to register a converted tool makes it unavailable to the agent.

---

## Related Concepts

- [Tools and Dependency Injection](#)
- [Function Calling and Interoperability](#)
- [LangChain Tools Documentation](https://python.langchain.com/docs/modules/agents/tools/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Adapter Design Pattern](https://refactoring.guru/design-patterns/adapter)
- [Dependency Injection in Python](https://realpython.com/dependency-injection-python/)

---