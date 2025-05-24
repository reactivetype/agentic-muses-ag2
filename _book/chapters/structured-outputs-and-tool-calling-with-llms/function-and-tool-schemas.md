# Function and Tool schemas

## Overview

Function and Tool schemas enable Language Learning Models (LLMs) to interact with external tools and return structured data rather than just plain text. By defining functions and tools with [JSON Schema](https://json-schema.org/), developers can specify the expected parameters and output formats for tool calls, ensuring consistency, clarity, and error reduction in LLM-powered applications.

When LLMs are configured for **structured outputs** and **tool calling**, they can interpret system instructions to invoke external functions/tools with validated arguments, and provide predictable responses in a machine-readable format.

---

## Explanation

### What are Function and Tool Schemas?

A **Function/Tool Schema** is a formal definition, typically using JSON Schema, describing:

- The function/tool's name and description
- The required and optional parameters, their types, and constraints
- The expected output structure (for structured outputs)

This schema is registered with the LLM client or platform, allowing the model to:

- Understand which tools are available and how to use them
- Generate tool calls with arguments that conform to the schema
- Serialize outputs in a structured (e.g., JSON) format for downstream processing

### Why Use Function and Tool Schemas?

- **Safety:** Prevents malformed requests and responses.
- **Reliability:** Ensures LLM-generated tool invocations are valid.
- **Automation:** Enables downstream systems to parse and act on LLM outputs automatically.
- **Discoverability:** Allows LLMs (and users) to know what tools/functions are available and how to use them.

### Typical Workflow

1. **Define the function/tool schema** using JSON Schema.
2. **Register the schema** with the LLM client or orchestrator.
3. **Prompt the LLM** to use the tool or function by issuing tasks that require it.
4. **LLM generates a tool call** (sometimes called "function call") message with arguments.
5. **System validates and executes** the tool, and may return structured results.
6. **LLM continues the conversation** using the output as needed.

---

## Examples

### Example 1: Defining a Function Schema

Suppose we have a function `get_weather` that retrieves the weather for a given city and date.

```python
# Example in Python using OpenAI's function calling API

weather_schema = {
    "name": "get_weather",
    "description": "Get the weather forecast for a specific location and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and country, e.g. 'London, UK'"
            },
            "date": {
                "type": "string",
                "format": "date",
                "description": "The date to get the weather for (YYYY-MM-DD)"
            }
        },
        "required": ["location", "date"]
    }
}
```

### Example 2: Registering the Schema with an LLM Client

```python
import openai

# Assume you have set up your OpenAI client
openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[...],
    functions=[weather_schema],  # Register your function schemas here
    function_call="auto",        # Let the model decide when to call
)
```

### Example 3: Tool Call Message Flow

**User:**  
> What's the weather in Paris tomorrow?

**LLM Output (tool call):**
```json
{
  "tool_call": {
    "name": "get_weather",
    "arguments": {
      "location": "Paris, France",
      "date": "2024-06-08"
    }
  }
}
```

**System executes tool and returns:**
```json
{
  "location": "Paris, France",
  "date": "2024-06-08",
  "forecast": "Sunny, high of 25°C, low of 15°C"
}
```

**LLM continues:**  
> The weather in Paris tomorrow will be sunny, with a high of 25°C and a low of 15°C.

---

## Best Practices

- **Be Explicit:** Clearly define all parameter types, required fields, and descriptions in your schema.
- **Validate Inputs:** Always validate tool call arguments against the schema before execution.
- **Limit Scope:** Only expose necessary functions/tools to the LLM to minimize risk.
- **Use Structured Outputs:** Prefer JSON or similar formats for machine-readability.
- **Provide Clear Descriptions:** This helps both the LLM and human developers understand each tool.
- **Handle Errors Gracefully:** Ensure that error responses are also structured and documented.
- **Version Schemas:** Track changes to tool/function schemas to prevent breaking changes.

**Common Pitfalls:**

- Omitting required fields in the schema
- Using ambiguous parameter names or descriptions
- Allowing unvalidated tool calls to reach external systems
- Not updating schemas when tool signatures change

---

## Related Concepts

- [LLM Configuration and Model Clients](#)  
- [Tools and Dependency Injection](#)  
- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [JSON Schema Documentation](https://json-schema.org/)
- [Structured Outputs with LLMs](#)
- [Tool Call and Function Call Message Flows](#)
- [Prompt Engineering for Tool Use](#)

---

By defining and registering function and tool schemas, you enable LLMs to interact with the outside world in a safe, robust, and structured way, unlocking powerful automation and integration capabilities.