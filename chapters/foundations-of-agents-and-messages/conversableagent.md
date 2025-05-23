# ConversableAgent

## Overview

A `ConversableAgent` is an abstraction in agent-based systems that enables agents to communicate using structured messages. It defines a protocol allowing agents to send, receive, and process messages, facilitating collaboration, negotiation, or task delegation in multi-agent environments. The `ConversableAgent` extends a basic agent model by adding conversational capabilities, such as maintaining dialogue context and handling various message types and events.

## Explanation

In agent-oriented programming, agents are autonomous entities capable of perceiving their environment and acting upon it. While a simple agent may only react to environmental changes, a `ConversableAgent` is explicitly designed to interact with other agents through a structured messaging protocol.

### Key Features

- **Message-Based Communication:** Agents exchange information via messages that encapsulate data, intent, and metadata.
- **Event Handling:** Agents can handle events triggered by incoming messages or changes in conversation state.
- **Dialog Management:** Maintains the context of ongoing conversations, enabling multi-turn dialogues.
- **Extensibility:** Supports custom message types, protocols, and behaviors.

### Agent Protocol

The protocol typically defines:

- **Message Structure:** Standard fields like sender, recipient, content, and type.
- **Lifecycle Events:** Events such as message received, message processed, error, or timeout.
- **Communication Patterns:** One-to-one, broadcast, or request-response messaging.

### Class Hierarchy

- **Agent:** The base class for all agents. Handles basic perception and actions.
- **ConversableAgent:** Extends `Agent` with message handling and conversation management.

#### Example Class Skeleton

```python
class Agent:
    def act(self, observation):
        pass  # Basic action logic

class ConversableAgent(Agent):
    def send_message(self, recipient, message):
        pass  # Logic for sending a message

    def receive_message(self, message):
        pass  # Logic for receiving a message

    def handle_event(self, event):
        pass  # Custom event handling
```

### Message and Event Structure

A typical message might be represented as a dictionary or a custom object:

```python
message = {
    "sender": "agent_1",
    "recipient": "agent_2",
    "type": "inform",
    "content": "Task completed.",
    "timestamp": "2024-06-15T12:00:00Z"
}
```

Events might be triggered by message reception or conversation state changes:

```python
event = {
    "type": "message_received",
    "message": message
}
```

## Examples

### Example 1: Basic ConversableAgent

```python
class ConversableAgent(Agent):
    def __init__(self, name):
        self.name = name
        self.inbox = []

    def send_message(self, recipient, content):
        message = {
            "sender": self.name,
            "recipient": recipient.name,
            "content": content
        }
        recipient.receive_message(message)

    def receive_message(self, message):
        print(f"{self.name} received: {message['content']} from {message['sender']}")
        self.inbox.append(message)
        self.handle_event({"type": "message_received", "message": message})

    def handle_event(self, event):
        if event["type"] == "message_received":
            print(f"{self.name} handling event: {event}")
```

**Usage:**

```python
alice = ConversableAgent("Alice")
bob = ConversableAgent("Bob")

alice.send_message(bob, "Hello, Bob!")
# Output:
# Bob received: Hello, Bob! from Alice
# Bob handling event: {'type': 'message_received', ...}
```

### Example 2: Handling Different Message Types

```python
class AdvancedConversableAgent(ConversableAgent):
    def handle_event(self, event):
        message = event["message"]
        if message.get("type") == "request":
            self.process_request(message)
        elif message.get("type") == "inform":
            print(f"{self.name} was informed: {message['content']}")
        else:
            print(f"{self.name} received unknown message type.")

    def process_request(self, message):
        print(f"{self.name} processing request: {message['content']}")
        # Respond to request, etc.
```

## Best Practices

- **Define Clear Message Schemas:** Ensures all agents interpret messages consistently.
- **Maintain Conversation Context:** Use identifiers or state tracking for multi-turn dialogues.
- **Handle Unexpected Events:** Gracefully handle unknown message types or malformed messages.
- **Decouple Message Processing:** Separate message parsing from business logic for maintainability.
- **Limit Side Effects:** Keep message handlers isolated to prevent unintended agent behavior.

**Common Pitfalls:**

- Ignoring message type or metadata, leading to misinterpretation.
- Not validating message content, causing runtime errors.
- Allowing shared state between agents, breaking autonomy.

## Related Concepts

- **[Agent](#)**: The base abstraction for autonomous entities (see "Agent" documentation).
- **[Message Passing](https://en.wikipedia.org/wiki/Message_passing)**: The fundamental communication mechanism in agent systems.
- **[Event-Driven Programming](https://en.wikipedia.org/wiki/Event-driven_programming)**: Relevant for handling message and event callbacks.
- **[Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)**: Broader context for agent interactions.
- **[Protocol Design](https://en.wikipedia.org/wiki/Communication_protocol)**: For designing robust agent communication protocols.

---

*For further reading, refer to classic agent frameworks like [JADE](https://jade.tilab.com/) or libraries such as [spaCy's agent module](https://spacy.io/universe/project/spacy-agents) (if available).*