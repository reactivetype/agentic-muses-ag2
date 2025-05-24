# AgentCapability base class

## Overview

The `AgentCapability` base class is a foundational abstraction for building modular, composable, and extensible agents. It defines a standard interface for adding discrete skills (capabilities) to agents, enabling them to handle various modalities (such as vision or text), manage context, and support advanced features like teachability and vector memory. By designing capabilities as composable units, developers can create complex, multimodal agents with clear separation of concerns.

---

## Explanation

The `AgentCapability` base class encapsulates logic or skills that can be attached to an agent. Each capability provides specific methods or message handlers, which the agent can invoke during interaction. This pattern allows developers to:

- **Compose multiple capabilities:** An agent can be constructed with any combination of capabilities (e.g., vision, memory, reasoning).
- **Isolate functionality:** Each capability encapsulates its own state and logic, making the system maintainable and testable.
- **Enable teachability:** Capabilities can manage knowledge bases with vector memory for storing and retrieving information.
- **Handle context and conditional logic:** Capabilities can implement context-aware behaviors, transforming messages or responses as needed.

### Key Concepts

- **Abstract Interface:** Defines required methods (e.g., `handle_message`, `transform_message`).
- **Registration:** Capabilities are registered to an agent, which delegates tasks based on message types or context.
- **Composability:** Multiple capabilities can be combined, allowing agents to support a wide range of features.

### Example Structure

```python
class AgentCapability:
    """
    Base class for agent capabilities.
    """
    def handle_message(self, message, context):
        """
        Process incoming message and return a response.
        """
        raise NotImplementedError

    def transform_message(self, message, context):
        """
        Optionally transform the message based on context or state.
        """
        return message

    # Additional optional methods for teachability, memory, etc.
```

---

## Examples

### 1. Composing Capabilities into an Agent

```python
class Agent:
    def __init__(self, capabilities):
        self.capabilities = capabilities

    def handle(self, message, context):
        for capability in self.capabilities:
            # Each capability can decide if it should handle the message
            response = capability.handle_message(message, context)
            if response is not None:
                return response
        return "I don't know how to handle that."

# Example vision capability
class VisionCapability(AgentCapability):
    def handle_message(self, message, context):
        if 'image' in message:
            return "I see an image!"
        return None

# Example memory capability
class VectorMemoryCapability(AgentCapability):
    def __init__(self):
        self.memory = []

    def handle_message(self, message, context):
        if message.get('teach'):
            self.memory.append(message['teach'])
            return "Knowledge stored."
        if message.get('recall'):
            # Perform vector search (pseudo-code)
            return f"Closest match: {self.memory[0]}"
        return None

# Compose agent
agent = Agent([
    VisionCapability(),
    VectorMemoryCapability(),
])

# Use agent
agent.handle({'image': '...'}, {})
agent.handle({'teach': 'The sky is blue.'}, {})
```

### 2. Message Transformation for Context Management

```python
class ContextTransformCapability(AgentCapability):
    def transform_message(self, message, context):
        # Add user info based on context variable
        if 'user_id' in context:
            message['user'] = context['user_id']
        return message

# In agent loop:
for capability in agent.capabilities:
    message = capability.transform_message(message, context)
```

---

## Best Practices

- **Single Responsibility:** Implement one logical skill per capability to maintain clarity.
- **Explicit Registration:** Register only the necessary capabilities for each agent to avoid unexpected behaviors.
- **Message Routing:** Use clear conventions for when a capability should handle or transform a message.
- **Statelessness When Possible:** Keep capabilities stateless unless necessary (e.g., for memory).
- **Testing:** Unit test each capability in isolation before composing them.
- **Context Awareness:** Use context variables and conditional logic to enable dynamic behaviors.

**Common Pitfalls:**

- Overlapping responsibilities between capabilities, leading to ambiguous handling.
- Not handling context propagation consistently, causing context loss.
- Making capabilities too tightly coupled, reducing reusability.

---

## Related Concepts

- [Multimodal and Vision Capabilities](#)
- [Context Variables and Conditional Logic](#)
- [Teachability and Vector Memory](#)
- [Message Transforms](#)
- [Agent Architecture Patterns](#)
- [Handler Chains and Middleware](#)

For further reading, see:

- [Design Patterns: Strategy and Chain of Responsibility](https://refactoring.guru/design-patterns/strategy)
- [Composable AI Agents](https://ai.stackexchange.com/questions/22381/what-are-composable-ai-agents)
- [Vector Memory in AI Agents](https://www.pinecone.io/learn/vector-database/)

---