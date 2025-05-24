# Tool abstraction

## Overview

**Tool abstraction** is a pattern that encapsulates functions or methods as "tools" that can be invoked by an agent within a workflow, such as a conversable agent. This abstraction enables agents to perform actions, fetch data, or interact with the environment in a controlled and extensible way. Through tool abstraction, developers can inject dependencies (like database connections or APIs) and contextual information (like user sessions), making tools reusable, testable, and easy to register in a toolkit.

## Explanation

In the context of agent workflows, tools are callable objects (typically functions or classes) that perform specific tasks. Tool abstraction involves wrapping these callables in a way that the agent can discover, select, and execute them as needed, often based on user input or internal logic.

**Key aspects of tool abstraction:**

- **Wrapping Functions as Tools:** Functions are decorated or registered to be discoverable and invocable by the agent.
- **Dependency Injection:** Tools can require external services (such as databases, APIs, or configuration objects). Instead of hard-coding these, dependencies are injected, improving testability and modularity.
- **Context Injection:** Tools may need access to runtime context (e.g., user information, session state). Tool abstraction provides mechanisms to inject this context automatically.
- **Toolkit and Registration Mechanisms:** Tools are organized into toolkits or registries. This allows agents to access a dynamic set of capabilities and makes it easy to add, remove, or replace tools.

**Example workflow:**
1. Define a function (the tool's logic).
2. Register or decorate the function to make it a tool.
3. Inject dependencies and context as parameters.
4. Add the tool to a toolkit.
5. The agent dynamically selects and invokes the tool as needed.

## Examples

### 1. Wrapping a Function as a Tool

```python
from agent_framework.toolkit import tool

@tool(name="weather_info", description="Get weather for a city")
def get_weather(city: str, weather_client):
    return weather_client.get_current_weather(city)
```

### 2. Injecting Dependencies

```python
class WeatherClient:
    def get_current_weather(self, city):
        # Call weather API
        pass

weather_client = WeatherClient()

@tool(name="weather_info")
def get_weather(city: str, weather_client=weather_client):
    return weather_client.get_current_weather(city)
```

### 3. Injecting Context

```python
@tool(name="personalized_greeting")
def greet_user(context):
    user_name = context.get("user_name", "there")
    return f"Hello, {user_name}!"
```

### 4. Tool Registration in a Toolkit

```python
from agent_framework.toolkit import Toolkit

toolkit = Toolkit()
toolkit.register(get_weather)
toolkit.register(greet_user)

agent = ConversableAgent(toolkit=toolkit)
```

### 5. Dependency Injection via Tool Factory

```python
def create_database_tool(db):
    @tool(name="fetch_user")
    def fetch_user(user_id):
        return db.get_user(user_id)
    return fetch_user

toolkit.register(create_database_tool(database_instance))
```

## Best Practices

- **Keep Tools Atomic:** Tools should do one thing well to maximize reuse.
- **Define Clear Interfaces:** Specify input and output types for tools to aid agent reasoning and validation.
- **Inject, Don't Hardcode:** Use dependency and context injection to keep tools decoupled from their environment.
- **Document Tools Thoroughly:** Use descriptions and type annotations to help agents and developers understand tool capabilities.
- **Organize Tools Logically:** Group related tools in toolkits for easier management and discovery.
- **Handle Errors Gracefully:** Ensure tools return informative errors or exceptions for agent handling.
- **Avoid Side Effects:** Unless intentional, tools should minimize side effects to simplify reasoning and testing.

## Related Concepts

- [Conversable Agent Workflow](./Conversable-Agent-Workflow.html)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- [Toolkit Design Pattern](https://en.wikipedia.org/wiki/Toolkit_(software))
- [Tool Registration](./Tool-Registration.html)
- [Context Management](./Context-Management.html)
- [Agent Function Calling](./Agent-Function-Calling.html)
- [Testing Tools and Agents](./Agent-Testing.html)

For further reading on dependency injection, see [Martin Fowler's article](https://martinfowler.com/articles/injection.html).