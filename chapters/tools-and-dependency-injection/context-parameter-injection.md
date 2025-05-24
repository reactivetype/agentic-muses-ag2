# Context parameter injection

## Overview

Context parameter injection is a powerful pattern in agent workflows that allows dynamic, runtime-provided data—such as user context, session data, or system resources—to be automatically supplied to tool functions invoked by a conversational agent. By leveraging context injection, you can design reusable tool functions that stay decoupled from the underlying agent framework, making dependency management and customization easier and more robust.

This approach is essential in agent frameworks that orchestrate tool use, as it enables agents to access up-to-date information or shared resources without hardcoding dependencies or polluting function signatures with unnecessary parameters.

---

## Explanation

### What is Context Parameter Injection?

In the context of agent toolkits, context parameter injection refers to the automatic provision of context-specific or dependency objects to tool functions at runtime. When an agent calls a tool (a function registered for agent use), the toolkit inspects the function's parameters and, if necessary, injects values from the current context. This is often achieved via parameter names, type annotations, or decorator metadata.

#### Why is it needed?

- **Decoupling:** Tool functions remain focused on their logic, not on fetching dependencies.
- **Flexibility:** Supports swapping or mocking dependencies for testing.
- **Extensibility:** New context parameters can be added without refactoring all tools.

### How does it work?

Most agent toolkits (e.g., LangChain, OpenAI Functions, custom frameworks) implement context injection by:

1. **Inspecting function signatures** to determine which parameters can/should be injected.
2. **Matching parameter names/types** with available context or dependency providers.
3. **Providing values** for those parameters automatically at invocation time.

For example, if a tool function accepts a `user_id` or a `db_session` parameter, the toolkit can automatically pass these from the current conversational context or dependency registry.

---

## Examples

### Basic Example: Injecting User Context

Suppose you have a tool function that greets a user by name:

```python
def greet_user(user_name: str):
    return f"Hello, {user_name}!"
```

If your agent workflow tracks the `user_name` in its context, you can configure the toolkit to inject it:

```python
# Pseudo-code for registering the tool with context injection
toolkit.register_tool(greet_user)

# When the agent needs to greet, the framework automatically calls:
greet_user(user_name=context["user_name"])
```

### Advanced Example: Injecting Dependencies

Suppose you have a function that queries a database via a session object:

```python
def fetch_user_profile(user_id: str, db_session):
    return db_session.get_profile(user_id)
```

You can declare `db_session` as a context-injectable dependency:

```python
# During agent initialization
toolkit.register_dependency('db_session', db_session_instance)
toolkit.register_tool(fetch_user_profile)

# On invocation:
fetch_user_profile(user_id="123", db_session=toolkit.resolve('db_session'))
```

### Using Decorators for Injection

Some frameworks use decorators for more explicit injection:

```python
from some_agent_framework import tool, inject

@tool
def get_weather(location: str, weather_api=inject()):
    return weather_api.get_forecast(location)
```

Here, `inject()` tells the framework to supply the `weather_api` instance at runtime.

---

## Best Practices

- **Keep tool function signatures explicit**: Clearly define which parameters are to be injected versus those provided by the agent/user.
- **Avoid hardcoding dependencies**: Rely on context injection rather than global variables or singleton patterns.
- **Document required context parameters**: Make it clear which context keys or types are expected for each tool.
- **Test tools in isolation**: Use mock context/dependencies to ensure tools behave correctly when injected.
- **Limit context scope**: Only inject what is necessary to avoid leaking sensitive data or increasing coupling.

**Common Pitfalls:**

- **Name/Type mismatches**: Ensure parameter names/types align with what the toolkit/context provides.
- **Over-injection**: Don't inject more dependencies than needed—keep tools focused.
- **Silent failures**: Some frameworks may silently ignore missing context, leading to confusing bugs. Prefer explicit errors.

---

## Related Concepts

- [Tool registration and discovery](#)
- [Dependency injection patterns in Python](https://realpython.com/python-dependency-injection/)
- [Conversable Agent Workflow](#)
- [Function wrapping and decorators](https://docs.python.org/3/library/functools.html)
- [Agent toolkits and plugin architectures](#)

*For deeper dives, see:*
- [LangChain: Tool and Dependency Management](https://python.langchain.com/docs/modules/agents/tools/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Python’s inspect module](https://docs.python.org/3/library/inspect.html) (for introspection techniques)

---

By mastering context parameter injection, you enable agents to leverage dynamic, context-aware tools, making workflows more adaptable, maintainable, and robust.