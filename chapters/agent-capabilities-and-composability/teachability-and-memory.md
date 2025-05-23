# Teachability and memory

## Overview

Teachability and memory are foundational aspects of modern AI agent design, enabling agents not only to learn from user input but also to remember and utilize prior interactions. By equipping agents with teachable behaviors and vector-based memory, developers can create dynamic, adaptive systems that personalize responses, retain knowledge over time, and integrate new skills or concepts on-the-fly. Composability further allows these capabilities to be combined with other agent functionalities, such as multimodal processing and context-aware logic, to produce robust and flexible agents.

---

## Explanation

### Teachability

Teachability refers to an agent's ability to update its knowledge base or behavior in response to user instructions or new information, without requiring developer intervention. This empowers users to "teach" the agent new facts, preferences, or tasks during conversations.

### Memory

Memory enables agents to store, retrieve, and leverage information from past interactions. Vector memory, in particular, utilizes vector embeddings to represent and recall knowledge efficiently, supporting semantic search and contextual retrieval. This allows agents to remember not just exact phrases, but also related concepts and meanings.

### Composability

Agents can combine teachability and memory with other capabilities (e.g., vision, multimodal analysis, conditional logic) to deliver richer, more context-aware experiences.

#### Example Workflow

1. **User teaches agent a new fact:** "My favorite color is teal."
2. **Agent stores this as a vector embedding** in its memory.
3. **Later, agent is asked:** "What color do I like?"
4. **Agent retrieves relevant memory** and responds: "Your favorite color is teal."

### Message Transforms

Message transforms are mechanisms applied to incoming/outgoing messages, enabling context management, memory updates, or custom processing steps. For example, a transform might tag messages with user IDs, preprocess inputs, or inject retrieved memories into prompts.

---

## Examples

### Example 1: Composing Capabilities in a Teachable Agent

```python
from agent_framework import Agent, VectorMemory, Teachability, Vision, Multimodal, ContextManager

# Compose capabilities
memory = VectorMemory(size=2048)
teachability = Teachability(memory=memory)
vision = Vision()
multimodal = Multimodal()

# Define agent with multiple capabilities
agent = Agent(
    capabilities=[teachability, memory, vision, multimodal],
    context_manager=ContextManager()
)
```

### Example 2: Teaching and Recalling Knowledge

```python
# Teach the agent
user_message = "My cat's name is Whiskers."
agent.process(user_message)  # Agent stores fact in vector memory

# Ask the agent a related question
query = "What is my cat's name?"
response = agent.process(query)
print(response)  # "Your cat's name is Whiskers."
```

### Example 3: Message Transform for Context Management

```python
def inject_relevant_memories(message, agent):
    # Retrieve related memories based on current message
    memories = agent.memory.search(message, top_k=3)
    # Append memories to message context
    message.context['retrieved_memories'] = memories
    return message

# Register transform
agent.context_manager.add_transform(inject_relevant_memories)
```

---

## Best Practices

- **Isolate Teachability Logic:** Separate teachable behavior from core agent logic for maintainability.
- **Use Vector Embeddings for Memory:** Enables fuzzy retrieval and semantic matching, not just keyword search.
- **Limit Memory Size:** Implement memory pruning or summarization to control storage and performance.
- **Apply Contextual Transforms:** Use message transforms to manage context, inject relevant memories, and avoid context bloat.
- **Handle Sensitive Data Carefully:** Ensure memory does not inadvertently retain private or sensitive information.
- **Test Composability:** Validate that multiple capabilities work harmoniously and do not introduce unintended side effects.

**Common Pitfalls:**
- Forgetting to update or clear memory when needed
- Overloading context with irrelevant information
- Failing to handle conflicting user instructions

---

## Related Concepts

- [Multimodal and Vision Capabilities](./multimodal-and-vision-capabilities.md)
- [Context Variables and Conditional Logic](./context-variables-and-conditional-logic.md)
- [Prompt Engineering](./prompt-engineering.md)
- [Stateful vs. Stateless Agents](./stateful-vs-stateless-agents.md)
- [Memory Management Strategies](./memory-management-strategies.md)
- [Knowledge Graphs and Semantic Search](./knowledge-graphs-and-semantic-search.md)

For further reading:
- [OpenAI Cookbook: Vector Databases & Memory](https://cookbook.openai.com/)
- [LangChain: Memory Concepts](https://python.langchain.com/docs/modules/memory/)
- [Message Passing and Middleware in Agent Frameworks](https://docs.microsoft.com/en-us/azure/architecture/patterns/message-broker)