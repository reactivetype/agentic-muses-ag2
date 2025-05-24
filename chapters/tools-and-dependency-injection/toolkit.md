# Toolkit

## Overview

The **Toolkit** is a core abstraction in agent-based frameworks that enables agents to interact with the world by exposing functions as **tools**. These tools are callable operations—such as data queries, web searches, or business logic functions—that the agent can invoke as needed during its workflow. The toolkit handles the **registration** of these functions and facilitates **dependency injection**, allowing agents to access contextual information or shared resources without tight coupling.

By wrapping functions as tools and injecting dependencies, you create a modular, maintainable, and extensible system where agents can dynamically compose capabilities to solve complex tasks.

---

## Explanation

### What is a Tool?

A **tool** is a function or callable that an agent can use to perform specific actions. Tools are typically annotated with metadata (e.g., name, description, input/output schemas) so that agents can reason about which tools to use and how to invoke them.

### What is a Toolkit?

A **toolkit** is a container or registry for tools. It manages:

- **Tool registration**: Adding, removing, and listing available tools.
- **Dependency injection**: Supplying tools with the required context or resources at runtime.
- **Interface abstraction**: Presenting a unified interface for agent workflows.

### Dependency Injection in Toolkits

Dependency injection enables you to write functions that require certain resources or context (e.g., a database connection, user session, configuration). Instead of hardcoding these dependencies, the toolkit provides them at runtime, making your tools more reusable and testable.

#### Example Workflow

1. **Define a function**: Annotate it as a tool, specifying its name and description.
2. **Register the function**: Add it to the toolkit.
3. **Agent Execution**: The agent selects and invokes tools as needed, with the toolkit handling dependency injection.

---

## Examples

### 1. Wrapping a Function as a Tool

```python
from my_agent_framework import tool

@tool(name='Get Weather', description='Fetches the current weather for a given city.')
def get_weather(city: str, weather_api_client):
    return weather_api_client.fetch(city)
```

### 2. Registering Tools in a Toolkit

```python
from my_agent_framework import Toolkit

toolkit = Toolkit()
toolkit.register(get_weather)
```

### 3. Injecting Dependencies

Suppose `get_weather` needs a `weather_api_client`. The toolkit can inject this when the tool is called:

```python
weather_api_client = WeatherAPIClient(api_key="SECRET")

toolkit.provide('weather_api_client', weather_api_client)

# When the agent uses the tool, the dependency is injected automatically:
result = toolkit.invoke('Get Weather', city='San Francisco')
```

### 4. Agent Using the Toolkit

```python
agent = ConversableAgent(toolkit=toolkit)
response = agent.run("What's the weather in San Francisco?")
```

---

## Best Practices

- **Keep tools single-purpose**: Each tool should do one thing well.
- **Use explicit names and descriptions**: This helps agents (and humans) understand available capabilities.
- **Leverage dependency injection**: Avoid hardcoding dependencies; let the toolkit manage resources.
- **Register tools modularly**: Group related tools into separate toolkits for maintainability.
- **Document input/output schemas**: Specify what each tool expects and returns for seamless agent integration.
- **Test tools independently**: Since dependencies are injected, tools can be easily tested in isolation.

**Common Pitfalls:**

- **Overloading tools**: Avoid making tools too complex or multipurpose.
- **Circular dependencies**: Ensure injected dependencies do not create dependency cycles.
- **Unclear metadata**: Missing or unclear tool descriptions hinder agent reasoning.

---

## Related Concepts

- [Conversable Agent Workflow](#)
- [Dependency Injection](#)
- [Tool Registration](#)
- [Function Annotation](#)
- [Prompt Engineering for Agents](#)
- [Tool Chaining and Composition](#)
- [Testing Tools and Toolkits](#)

> For more information, see: [Agent Tools and Toolkits: Patterns and Practices](https://example.com/agent-toolkit-patterns)

---