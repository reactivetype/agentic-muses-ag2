# Reply function registration

## Overview

Reply function registration is a core mechanism that enables an agent to respond dynamically to incoming messages. By registering reply functions, developers can specify how an agent should react to specific message types, content, or triggers during a conversation. This process allows for modular, maintainable, and context-aware conversation flows, supporting both automated responses and integrating human input where necessary.

---

## Explanation

In a conversable agent workflow, **reply functions** are callbacks or handlers that the agent invokes in response to certain messages or triggers. Registration is the process of associating these functions with specific message patterns, types, or conditions.

**How it works:**
- An agent maintains a registry (often a mapping or list) of reply functions and their associated triggers.
- When a message is received, the agent scans the registry to determine if any function should be triggered based on the message's characteristics (e.g., type, intent, content).
- If a match is found, the corresponding function is executed, producing a reply or initiating an action.
- Reply functions can be chained or composed to build complex conversational workflows, including branching, loops, and human-in-the-loop steps.

**Human input modes:**  
Agents can be configured to switch between automated reply functions and modes that solicit human input (e.g., pausing for a human operator to respond), allowing for hybrid workflows.

---

## Examples

### 1. Basic Reply Function Registration

```python
def greet(message):
    return "Hello! How can I help you today?"

agent.register_reply(trigger="greeting", function=greet)
```

When a message with the type or intent `"greeting"` arrives, the `greet` function is called.

---

### 2. Reply Function with Message Pattern Matching

```python
def handle_order(message):
    item = message.get('item')
    return f"Sure, I will help you order {item}."

agent.register_reply(trigger=lambda msg: "order" in msg.text, function=handle_order)
```

Here, the reply function is triggered if the message contains the word `"order"`.

---

### 3. Human Input Mode Integration

```python
def escalate_to_human(message):
    agent.set_human_input_mode(True)
    return "I'm connecting you to a human agent. Please wait..."

agent.register_reply(trigger="escalation", function=escalate_to_human)
```

The agent switches to a human input mode, pausing automated replies until a human responds.

---

### 4. Sequential Reply Functions (Workflow)

```python
def ask_name(message):
    agent.expect_reply(trigger="user_name", function=save_name)
    return "What is your name?"

def save_name(message):
    agent.state['name'] = message.text
    return f"Nice to meet you, {message.text}!"

agent.register_reply(trigger="start", function=ask_name)
```

The agent first asks for the user's name, then registers a new reply function for the next expected input.

---

## Best Practices

- **Be specific with triggers:** Use precise message types or patterns to avoid unintended replies.
- **Avoid overlapping triggers:** Ensure that multiple reply functions do not compete for the same message unless intended.
- **Manage state:** Store relevant context in the agent's state to support multi-turn conversations.
- **Handle human input transitions gracefully:** Clearly indicate to users when the agent is switching between automated and human responses.
- **Test complex workflows:** Simulate various conversation flows to catch unexpected behaviors or dead ends.
- **Document registered functions:** Maintain clear documentation for each registered reply function and its trigger for maintainability.

**Common Pitfalls:**
- Registering multiple functions for the same trigger without clear priority.
- Forgetting to unregister or update reply functions, causing stale or repeated responses.
- Not handling edge cases where no reply function matches the incoming message.

---

## Related Concepts

- [Agent State Management](#)
- [Message Triggers and Patterns](#)
- [Human-in-the-Loop Workflows](#)
- [Conversation Flow Control](#)
- [Advanced Reply Function Composition](#)

For more foundational information, see:  
- [Foundations of Agents and Messages](#)

---

This documentation should provide a solid foundation for understanding and implementing reply function registration in conversable agent workflows.