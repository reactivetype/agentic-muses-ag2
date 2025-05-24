# BaseMessage and message serialization

## Overview

In agent-based systems, **agents** communicate by exchanging structured data known as _messages_. The **BaseMessage** class typically defines the foundation for all messages exchanged between agents. To facilitate communication, these messages are often **serialized**—converted into a format suitable for transmission or storage (e.g., JSON or binary). Understanding the structure of `BaseMessage` and the process of message serialization is fundamental to building robust and interoperable agent systems.

---

## Explanation

### The Agent Protocol

Agents operate by sending and receiving messages. The agent protocol typically defines:
- **Message format:** How is information structured?
- **Serialization:** How is the message converted to/from a transmittable format?
- **Deserialization:** How is the message reconstructed on receipt?

### BaseMessage Structure

A `BaseMessage` class generally contains:
- **Metadata** (e.g., sender, recipient, timestamp)
- **Message type** (e.g., "event", "command", "response")
- **Payload** (the actual content of the message)

#### Example Structure (pseudocode)

```python
class BaseMessage:
    def __init__(self, sender, recipient, msg_type, payload, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.msg_type = msg_type
        self.payload = payload
        self.timestamp = timestamp or datetime.now()
```

### Message Serialization

**Serialization** is the process of converting an object (like `BaseMessage`) into a format (string or bytes) that can be sent over a network or saved to disk. The most common formats are:
- **JSON** (human-readable, widely supported)
- **Pickle** (Python-specific, not secure for untrusted data)
- **Protobuf/MessagePack** (efficient, binary)

**Deserialization** is the reverse: reconstructing the object from its serialized form.

#### Why Serialization?

- **Interoperability**: Agents may run in different environments or languages.
- **Persistence**: Messages can be stored and replayed.
- **Transmission**: Data must be in a standard format to send over a network.

### Distinguishing Agent Classes

Agent classes may handle messages differently:
- **Reactive agents:** Respond to events or messages.
- **Deliberative agents:** Plan actions based on received messages.
- **Hybrid agents:** Combine multiple behaviors.

---

## Examples

### Defining a BaseMessage Class

```python
import json
from datetime import datetime

class BaseMessage:
    def __init__(self, sender, recipient, msg_type, payload, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.msg_type = msg_type
        self.payload = payload
        self.timestamp = timestamp or datetime.now().isoformat()

    def serialize(self):
        return json.dumps({
            'sender': self.sender,
            'recipient': self.recipient,
            'msg_type': self.msg_type,
            'payload': self.payload,
            'timestamp': self.timestamp,
        })

    @classmethod
    def deserialize(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls(**data)
```

### Sending and Receiving Messages

```python
# Creating a message
msg = BaseMessage(
    sender="AgentA",
    recipient="AgentB",
    msg_type="event",
    payload={"event_type": "temperature_update", "value": 22.5}
)

# Serialize for sending
serialized_msg = msg.serialize()
print("Serialized:", serialized_msg)

# On the receiving end
received_msg = BaseMessage.deserialize(serialized_msg)
print("Deserialized:", received_msg.payload)
```

### Customizing Message Types

```python
class EventMessage(BaseMessage):
    def __init__(self, sender, recipient, payload, timestamp=None):
        super().__init__(sender, recipient, 'event', payload, timestamp)
```

---

## Best Practices

- **Use clear and consistent message schemas.** All agents should agree on message structure.
- **Prefer human-readable serialization (like JSON) for debugging.** Use binary formats for efficiency only when necessary.
- **Validate messages on receipt.** Ensure required fields are present and types are correct.
- **Avoid using insecure serialization formats (e.g., Pickle) for untrusted data.**
- **Handle versioning.** If your message schema evolves, include version info for backward compatibility.
- **Log serialized messages for traceability and debugging.**

---

## Related Concepts

- [Agent Protocols](https://en.wikipedia.org/wiki/Agent_communication_language)
- [Agent Classes](https://en.wikipedia.org/wiki/Intelligent_agent#Types_of_agents)
- [Events and Event Handling](https://en.wikipedia.org/wiki/Event-driven_programming)
- [Serialization in Python (docs)](https://docs.python.org/3/library/json.html)
- [Message-Oriented Middleware](https://en.wikipedia.org/wiki/Message-oriented_middleware)
- [Protobuf (Protocol Buffers)](https://developers.google.com/protocol-buffers)

---