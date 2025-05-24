# Chat message flow

## Overview

The **chat message flow** is a core concept in building conversational agents. It refers to how messages are exchanged between users and agents, how agents determine when and how to reply, and how human input is handled within the conversation. By mastering chat message flow, developers can design agents that respond intelligently, maintain context, and enable complex interaction patterns.

---

## Explanation

A conversational agent operates by listening for incoming messages, determining whether it should reply, and generating responses accordingly. The message flow involves several key components:

- **Message triggers:** Rules or functions that determine when the agent should respond.
- **Reply functions:** Functions registered to handle specific types of messages or triggers.
- **Human input modes:** Methods for incorporating user input at various stages of the conversation.

### 1. Registering and Triggering Reply Functions

Agents typically use a registration mechanism to associate specific functions with message patterns or triggers. When a message matches a trigger, the corresponding reply function is executed.

**Example triggers:**
- Message contains specific keywords ("help", "order status")
- Message comes from a particular user role (admin, guest)
- Message matches a regular expression or intent

### 2. Controlling Conversation Flow

By chaining triggers and reply functions, you can direct the flow of the conversation. You may prompt the user for more information, branch based on user input, or escalate to a human operator.

**Conversation flow controls:**
- Conditional branching
- Maintaining conversation state/context
- Looping for clarification or retries

### 3. Utilizing Human Input Modes

Agents may need to request specific types of input:
- **Free-text input:** Ask open-ended questions
- **Choice selection:** Provide options for the user to pick
- **File or media upload:** Request images, documents, etc.

These modes allow agents to handle diverse workflows, from simple Q&A to complex forms.

---

## Examples

### Registering a Reply Function

```python
def on_greeting(message, context):
    return "Hello! How can I help you today?"

agent.register_handler(trigger="greeting", handler=on_greeting)
```

### Triggering on Keywords

```python
def help_reply(message, context):
    return "Here are some things I can assist you with: ..."

agent.register_handler(trigger=lambda m: "help" in m.text.lower(), handler=help_reply)
```

### Requesting Human Input: Choice Selection

```python
def ask_for_service(message, context):
    return {
        "text": "Which service do you need?",
        "choices": ["Order Status", "Technical Support", "Other"]
    }

agent.register_handler(trigger="start", handler=ask_for_service)

def handle_service_choice(message, context):
    if message.text == "Order Status":
        return "Please provide your order number."
    elif message.text == "Technical Support":
        return "Describe your technical issue."
    else:
        return "How else may I assist you?"

agent.register_handler(trigger="service_choice", handler=handle_service_choice)
```

### Maintaining Conversation Context

```python
def ask_order_number(message, context):
    context['awaiting_order_number'] = True
    return "Please enter your order number."

def handle_order_number(message, context):
    if context.get('awaiting_order_number'):
        context['order_number'] = message.text
        context['awaiting_order_number'] = False
        return f"Looking up order {message.text}..."
```

---

## Best Practices

- **Explicit triggers:** Use clear and explicit triggers to avoid unexpected responses.
- **Context management:** Track conversation state to provide coherent multi-turn interactions.
- **User-friendly prompts:** Guide users with clear instructions and limited-choice inputs when appropriate.
- **Error handling:** Anticipate invalid or unexpected input and handle gracefully.
- **Separation of concerns:** Keep logic for triggers, reply functions, and state management modular.
- **Testing:** Regularly test conversation flows for edge cases and user experience.

---

## Related Concepts

- [Agent State and Context Management](#)
- [Message Triggers and Handlers](#)
- [Human-in-the-Loop Workflows](#)
- [Conversation Design Patterns](#)
- [Advanced Agent Orchestration](#)

For further reading, see:
- [Foundations of Agents and Messages](#)
- [Building Conversational Flows](#)
- [Designing for Human Input in Chatbots](#)