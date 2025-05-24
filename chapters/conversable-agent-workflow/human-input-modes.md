# Human input modes

## Overview

Human input modes define how a conversable agent interacts with human users during a dialogue. They determine when and how the agent pauses for, requests, or processes input from a user, allowing for flexible conversation flows. By configuring human input modes, developers can tailor agent behavior to suit a variety of workflows—from simple Q&A to complex, multi-turn interactions.

## Explanation

Conversable agents operate by processing messages and generating responses. In many scenarios, agents must interact with human users at specific points in a conversation. Human input modes specify how and when these interactions take place. They influence:

- **When the agent waits** for user input.
- **How the agent processes** incoming human messages.
- **How the conversation flow is controlled**, including triggers and branching.

Human input modes are typically managed via reply functions and message triggers. A reply function is registered with the agent to handle a specific human input, while message triggers define the conditions under which the agent should request or expect input.

Common human input modes include:

- **Prompted Input:** The agent issues a prompt and waits for user input before continuing.
- **Unprompted Input:** The agent can accept user input at any time, even outside of explicit prompts.
- **Conditional Input:** The agent requests input only if certain conditions are met.
- **Multi-step Input:** The agent engages in a sequence of prompts, collecting multiple inputs over a conversation.

### Example: Prompted Input Mode

When the agent needs information from a user, it can enter a prompted input mode:

```python
def ask_for_email(agent, message):
    agent.prompt("Please enter your email address:")
    agent.register_reply("user_email", handle_email_input)

def handle_email_input(agent, message):
    email = message.text
    # Validate email here
    agent.send_message(f"Thank you! We received your email: {email}")
```

### Message Triggers & Reply Functions

Reply functions are registered with specific triggers (such as message types, intent, or keywords). When a message matching a trigger arrives, the associated reply function is executed.

```python
agent.register_trigger("greeting", handle_greeting)

def handle_greeting(agent, message):
    agent.send_message("Hello! How can I help you today?")
    agent.register_reply("user_request", handle_request)
```

## Examples

### Example 1: Simple Prompted Input

```python
def start_registration(agent, message):
    agent.send_message("Welcome! Let's get started.")
    agent.prompt("What's your name?")
    agent.register_reply("user_name", handle_name)

def handle_name(agent, message):
    user_name = message.text
    agent.send_message(f"Nice to meet you, {user_name}!")
```

### Example 2: Multi-step Input with Validation

```python
def ask_for_age(agent, message):
    agent.prompt("How old are you?")
    agent.register_reply("user_age", handle_age)

def handle_age(agent, message):
    try:
        age = int(message.text)
        if age < 0:
            raise ValueError
        agent.send_message(f"Got it! You are {age} years old.")
    except ValueError:
        agent.prompt("Please enter a valid age (numbers only).")
        agent.register_reply("user_age", handle_age)
```

### Example 3: Unprompted Input Handling

```python
def handle_any_message(agent, message):
    if "help" in message.text.lower():
        agent.send_message("Sure, how can I assist you?")
    else:
        agent.send_message("I'm here if you need anything.")

agent.register_trigger("any_message", handle_any_message)
```

## Best Practices

- **Explicitly register reply functions:** Always pair prompts with reply handlers to avoid unhandled input.
- **Validate and sanitize user input:** Never assume user input is correct; always check and handle errors gracefully.
- **Avoid dead-ends:** Ensure every prompt and input mode leads to a clear next step or fallback.
- **Support interruption and correction:** Allow users to correct their input or change the flow if needed.
- **Use clear prompts:** Make it obvious to the user when input is expected and what format is required.
- **Decouple triggers and handlers:** Keep message triggers and reply functions modular for easier maintenance.

## Related Concepts

- [Agents and Messages](./foundations_agents_messages.md)
- [Reply Functions](./reply_functions.md)
- [Message Triggers](./message_triggers.md)
- [Conversation Flow Control](./conversation_flow_control.md)
- [Error Handling in Conversable Agents](./error_handling.md)

For more in-depth information, see the [Foundations of Agents and Messages](./foundations_agents_messages.md) chapter.