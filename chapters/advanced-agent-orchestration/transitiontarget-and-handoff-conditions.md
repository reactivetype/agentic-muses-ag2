# TransitionTarget and handoff conditions

## Overview

In advanced agent orchestration, **TransitionTarget** and **handoff conditions** are mechanisms to control how conversational turns and responsibilities are transferred between agents (or models) in a multi-agent system. These tools enable dynamic conversation flows, where the system can switch speakers, delegate tasks, or escalate issues based on context, user intent, or business logic. Effective use of transition targets and handoff conditions is essential for building robust, context-aware group chats and orchestrated agent workflows.

---

## Explanation

### TransitionTarget

A **TransitionTarget** defines the next agent or model to take over the conversation after a certain condition or event is met. It specifies which agent should become the new speaker, as well as any context or state to be carried forward. TransitionTargets are typically used within orchestration patterns to:

- Route a user's message to the most appropriate agent
- Implement escalation policies (e.g., from a bot to a human)
- Manage agent roles (e.g., expert, assistant, moderator)

#### Types of TransitionTargets

- **Direct**: Explicitly names the next agent.
- **Conditional**: Chooses the next agent based on conversation context or specific triggers.
- **Round-robin or Priority-based**: Selects the next agent from a list, using ordering rules.

### Handoff Conditions

**Handoff conditions** are rules or triggers that determine when a handoff (i.e., a transition) should occur. They are used to detect when the current agent should transfer control to another agent. Common handoff conditions include:

- **Intent Detection**: E.g., if the user's message contains "talk to human", handoff to a human agent.
- **Completion of Task**: E.g., after booking is confirmed, handoff to a feedback agent.
- **Error or Exception**: E.g., if the current agent is unable to answer, escalate.
- **After Work (Follow-up)**: E.g., after a main agent finishes, a support agent follows up.

#### Workflow

1. **Monitor**: The orchestrator monitors conversation state and agent responses.
2. **Evaluate**: Checks if any handoff conditions are met.
3. **Transition**: If a condition is met, the orchestrator uses the TransitionTarget to select the next agent.
4. **Carry Context**: Optionally, passes conversation state to the next agent.

---

## Examples

### Example 1: Direct Transition on Intent

Suppose you have two agents: `FAQBot` and `HumanSupport`.

```python
# Orchestration pseudocode
if user_message.intent == "human_support":
    TransitionTarget = "HumanSupport"
else:
    TransitionTarget = "FAQBot"
```

### Example 2: Conditional Handoff with After Work Transition

After `OrderAgent` confirms an order, handoff to `FeedbackAgent` for collecting user feedback.

```python
if context["order_confirmed"]:
    TransitionTarget = "FeedbackAgent"
```

### Example 3: Custom Speaker Selection

Using a round-robin pattern among a list of expert agents:

```python
expert_agents = ["ExpertA", "ExpertB", "ExpertC"]
current_index = (last_index + 1) % len(expert_agents)
TransitionTarget = expert_agents[current_index]
```

### Example 4: Orchestration Configuration (YAML)

```yaml
agents:
  - name: FAQBot
  - name: HumanSupport

orchestration:
  transitions:
    - condition: user_intent == "human_support"
      target: HumanSupport
    - condition: true  # default
      target: FAQBot
```

---

## Best Practices

- **Define clear handoff conditions:** Ambiguous rules can result in unexpected transitions.
- **Preserve context:** Ensure relevant information is passed to the next agent.
- **Avoid transition loops:** Prevent endless handoffs by tracking recent transitions.
- **Graceful fallback:** Always have a default agent or error handler.
- **Test orchestration logic:** Validate with varied scenarios and edge cases.
- **Monitor for handoff fatigue:** Too many transitions can confuse users.

---

## Related Concepts

- [Agent Orchestration Patterns](#)  
- [Speaker Selection Strategies](#)  
- [Multi-Agent Group Chat Design](#)  
- [Context Management in Conversations](#)  
- [Escalation Policies](#)  
- [LLM Configuration and Model Clients](#)  

For further reading, see the documentation on [Orchestration Patterns](#) and [After Work Transitions](#).