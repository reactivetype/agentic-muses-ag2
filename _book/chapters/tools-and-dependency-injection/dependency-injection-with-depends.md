# Dependency injection with Depends

## Overview

Dependency injection is a design pattern that allows for the decoupling of components by providing their dependencies externally rather than hard-coding them inside the components. In the context of agent workflows and toolkits, **Depends** is used to inject dependencies or contextual information into tool functions dynamically. This enables tools to access resources such as agent memory, configuration, or other services without tight coupling, facilitating modularity, reusability, and testability.

## Explanation

In a Conversable Agent Workflow, tools are functions registered to the agent that perform specific tasks. Sometimes, these functions require dependencies—like access to the agent's context, configuration parameters, or external services. Instead of passing these dependencies manually every time, you can use **Depends** as a declarative mechanism to specify dependencies, and the agent runtime will resolve and inject them automatically.

### How Does `Depends` Work?

- **Declaration:** You annotate a function argument with `Depends`, specifying either a dependency function or class.
- **Resolution:** When the tool is invoked, the agent inspects the signature. For each parameter using `Depends`, it calls the dependency provider (which itself can declare further dependencies), building the required call stack.
- **Injection:** The resolved values are injected into the tool function transparently.

This approach is inspired by frameworks like FastAPI and allows for flexible composition of tools and services.

## Examples

### Basic Tool Registration

```python
from agentkit import Agent, Toolkit, tool

@tool
def greet(name: str):
    return f"Hello, {name}!"
```

### Injecting Context via Depends

Suppose you want your tool to access the agent's current conversation context:

```python
from agentkit import Depends, ConversationContext, tool

def get_current_context(context: ConversationContext = Depends()):
    # Return or process the current context as needed
    return context

@tool
def summarize(context: ConversationContext = Depends(get_current_context)):
    # Use the injected context
    return f"Summary of conversation: {context.summary()}"
```

When `summarize` is called as a tool, the agent automatically resolves and injects the current conversation context.

### Chained Dependencies

Dependencies can themselves depend on other dependencies, enabling complex dependency graphs:

```python
def get_database_connection():
    # Returns a database connection object
    ...

def get_user_profile(user_id: str, db=Depends(get_database_connection)):
    # Fetches user profile using db connection
    ...

@tool
def user_greeting(user_profile=Depends(get_user_profile)):
    return f"Welcome, {user_profile['name']}!"
```

### Tool Registration in Toolkits

You can bundle tools and their dependencies into a Toolkit:

```python
class MyToolkit(Toolkit):
    @tool
    def echo(self, message: str):
        return message

    @tool
    def agent_status(self, context=Depends()):
        return f"Agent is handling: {context.active_task}"
```

Register the toolkit with your agent:

```python
agent = Agent(toolkits=[MyToolkit()])
```

## Best Practices

- **Keep functions pure where possible:** Use dependency injection to provide external data or services instead of global variables.
- **Reuse dependencies:** Factor out common dependencies as standalone providers to promote reuse.
- **Declare explicit dependencies:** Be explicit in your function signatures to make dependencies clear and maintainable.
- **Avoid deep dependency chains:** Excessively deep or circular dependencies can make debugging difficult.
- **Document dependencies:** Clearly document what each dependency provides and why it is needed.
- **Test with mocks:** Dependency injection makes it easier to substitute dependencies with mock objects during unit testing.

## Related Concepts

- [Conversable Agent Workflow](./conversable-agent-workflow.html)
- [Toolkit and Tool Registration](./toolkit-tool-registration.html)
- [Context Injection](./context-injection.html)
- [Tool Function Design](./tool-function-design.html)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control)
- [Unit Testing with Dependency Injection](./unit-testing-di.html)

---

By leveraging dependency injection with **Depends**, you can build flexible, maintainable, and testable tools for your Conversable Agent workflows.