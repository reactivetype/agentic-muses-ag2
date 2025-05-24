# LLMAgent

## Overview

An **LLMAgent** is a software entity designed to interact with large language models (LLMs) through a standardized agent protocol. LLMAgents communicate by sending and receiving structured messages, enabling complex workflows such as question answering, code generation, and task automation. The agent protocol ensures interoperability between various agent classes and message types, allowing seamless integration of different LLM-powered components.

## Explanation

LLMAgents are at the core of modern AI-driven applications, acting as intermediaries between users, other agents, and LLMs. They encapsulate logic for:

- Sending requests (prompts, commands)
- Receiving and processing responses (completions, actions)
- Managing multi-step interactions (conversation, tool use)

### Agent Protocol

The **agent protocol** defines how agents communicate:

- **Messages**: Structured data packets containing content, sender, receiver, and metadata.
- **Events**: Notifications about important occurrences (e.g., message received, error occurred).
- **Actions**: Special message types that trigger operations (e.g., calling a function, fetching data).

### Agent Classes

LLMAgents can be categorized based on their roles:

- **UserAgent**: Represents human input.
- **ToolAgent**: Interfaces with external tools or APIs.
- **LLMAgent**: Specializes in communicating with LLMs, parsing prompts, and interpreting responses.
- **CoordinatorAgent**: Manages workflows and message routing between agents.

### Message and Event Structure

A message typically includes:

- `sender`: The agent sending the message
- `receiver`: The agent or component intended to receive the message
- `content`: The main payload (text, data, command)
- `timestamp`: When the message was created
- `metadata`: Additional context (e.g., message type, priority)

Events log and notify the system about state changes or results, such as:

- Message delivered
- Error occurred
- Task completed

## Examples

### Basic LLMAgent Class

```python
class LLMAgent:
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm  # LLM interface (e.g., OpenAI API client)

    def send_message(self, receiver, content, metadata=None):
        message = {
            'sender': self.name,
            'receiver': receiver,
            'content': content,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        # send the message to the receiver (could be another agent or LLM)
        return message

    def receive_message(self, message):
        print(f"Received message: {message['content']}")
        # Process message and possibly generate a response
        if message['receiver'] == self.name:
            return self.respond(message)

    def respond(self, message):
        # Example: send content to LLM and return reply
        response = self.llm.generate(message['content'])
        return self.send_message(
            receiver=message['sender'],
            content=response,
            metadata={'response_to': message['metadata'].get('id')}
        )
```

### Message Structure Example

```python
message = {
    "sender": "UserAgent",
    "receiver": "LLMAgent",
    "content": "What is the weather today?",
    "timestamp": 1718412000.0,
    "metadata": {
        "id": "msg123",
        "type": "query"
    }
}
```

### Agent Communication Flow

1. **UserAgent** sends a query to **LLMAgent**.
2. **LLMAgent** processes the message and queries the LLM.
3. **LLMAgent** sends a response message back to **UserAgent**.

```python
user_agent = UserAgent("UserAgent")
llm_agent = LLMAgent("LLMAgent", llm=OpenAIClient())

# User initiates conversation
msg = user_agent.send_message("LLMAgent", "Tell me a joke.")

# LLMAgent receives and processes
reply = llm_agent.receive_message(msg)
```

## Best Practices

- **Use clear message structures**: Ensure all messages include sender, receiver, content, and metadata.
- **Handle errors gracefully**: Implement event notifications for errors (e.g., invalid input, LLM failure).
- **Log events**: Keep track of message exchanges and agent actions for debugging.
- **Separate concerns**: Distinguish agent classes by role (e.g., don't combine tool and LLM logic in one agent).
- **Ensure extensibility**: Design the agent protocol and classes for easy addition of new agent types or message formats.

**Common Pitfalls:**

- Neglecting to handle unexpected message types or missing metadata.
- Tight coupling between agent logic and LLM backend.
- Failing to track message state, leading to lost or duplicate responses.

## Related Concepts

- [Agent Protocol](./agent-protocol.html)
- [Messages and Events](./messages-and-events.html)
- [ToolAgent](./toolagent.html)
- [CoordinatorAgent](./coordinatoragent.html)
- [Prompt Engineering](./prompt-engineering.html)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)

For further reading, see [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system) and [Design Patterns for Conversational Agents](https://arxiv.org/abs/2302.12346).