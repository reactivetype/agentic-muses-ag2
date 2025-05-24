# Tool call and function call message handling

## Overview

Tool call and function call message handling refers to the process by which Large Language Models (LLMs) are empowered to interact with external functions, APIs, or "tools" during a conversation. By defining and registering functions with a JSON schema, developers can enable LLMs to produce structured outputs that trigger specific actions, such as querying databases, fetching information, or performing calculations. This process involves configuring the LLM to recognize tool calls, formatting responses for downstream consumption, and managing the full message flow between user, model, and tools.

---

## Explanation

### 1. Defining and Registering Functions

To enable LLMs to call functions, each function (or "tool") must be registered with a schema that defines its name, description, and parameters using JSON Schema. This schema informs the model about what functions are available, their arguments, and how to format calls.

**Example schema:**

```json
{
  "name": "get_weather",
  "description": "Retrieve current weather information for a city.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "Name of the city"
      }
    },
    "required": ["city"]
  }
}
```

### 2. Configuring Structured Outputs

When configured for structured outputs, the LLM returns a special output format (often as a JSON object or via a specific message protocol). This output includes details about the function to call and its arguments, rather than plain text.

**Example output:**

```json
{
  "tool_calls": [
    {
      "name": "get_weather",
      "arguments": {
        "city": "Paris"
      }
    }
  ]
}
```

### 3. Message Flow Management

The typical message flow for tool/function calling is:

1. **User sends input:**  
   E.g., "What's the weather in Paris?"

2. **LLM responds with tool call:**  
   - Structured output indicating which tool to invoke and with what arguments.

3. **Application invokes tool:**  
   - Backend extracts tool call from model output.
   - Calls the corresponding registered function with provided arguments.

4. **Application returns results to LLM (optional):**  
   - Sends results back to LLM as a function result message for further reasoning or response synthesis.

5. **LLM produces final user-facing response:**  
   - E.g., "The weather in Paris is 22°C and sunny."

---

## Examples

### Python Example Using OpenAI API

#### Registering a function

```python
from openai import OpenAI

client = OpenAI()

functions = [
    {
        "name": "get_weather",
        "description": "Retrieve current weather information for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"]
        }
    }
]
```

#### Sending a tool call enabled request

```python
response = client.chat.completions.create(
    model="gpt-4-0613",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=functions,
    tool_choice="auto"  # or specify a tool if needed
)

tool_calls = response.choices[0].message.tool_calls
```

#### Handling the tool call

```python
def get_weather(city):
    # Dummy function for demonstration
    return f"The weather in {city} is 22°C and sunny."

for call in tool_calls:
    if call.name == "get_weather":
        result = get_weather(**call.arguments)
        # Send function result back to the LLM if further reasoning is desired
        # Or format the final response for the user
```

### Message Flow Diagram

```text
User Input  -->  LLM (Tool Call Output)  -->  App (Tool Invocation)  -->  LLM (Optional Reasoning)  -->  Final Response
```

---

## Best Practices

- **Define clear, unambiguous schemas:** Use descriptive names and parameter descriptions to help the LLM choose and populate tools correctly.
- **Validate input and output:** Always validate that the LLM's tool call arguments match your schema before invoking a function.
- **Handle errors gracefully:** Prepare for missing or malformed arguments, tool failures, or ambiguous LLM responses.
- **Limit tool exposure:** Only register functions that should be accessible to the model to minimize risk.
- **Chain tool calls carefully:** If using multiple tools or multi-step reasoning, manage message state and context explicitly.
- **Monitor usage:** Log tool calls and monitor for unexpected or malicious use.
- **Version your schemas:** If your function signatures change, version them to maintain backward compatibility.

---

## Related Concepts

- [Structured Outputs with LLMs](#)  
- [LLM Configuration and Model Clients](#)
- [Tools and Dependency Injection](#)
- [Function Calling in OpenAI API](https://platform.openai.com/docs/guides/function-calling)
- [JSON Schema](https://json-schema.org/)
- [Prompt Engineering for Tool Use](#)
- [Chaining and Orchestration with LLMs](#)

---