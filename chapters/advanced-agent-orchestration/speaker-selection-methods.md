# Speaker selection methods

## Overview

Speaker selection methods are strategies used in advanced agent orchestration to determine which agent (or "speaker") should respond at a given turn in a group chat or multi-agent environment. Proper speaker selection is essential for enabling effective collaboration, coherent task execution, and seamless transitions between agents in complex conversations or workflows. These methods can be rule-based, probabilistic, or context-aware, and are often customized to fit specific orchestration patterns such as handoff, round-robin, or dynamic role assignment.

---

## Explanation

In multi-agent systems, "agents" can represent different LLMs, specialized bots, or user personas. When orchestrating a group chat, the system must decide which agent should "speak" next. The speaker selection method governs this decision, ensuring that:

- The right agent handles the right part of the conversation
- The flow of conversation remains logical and efficient
- Agents can hand off tasks or provide after-action summaries as needed

**Common Speaker Selection Patterns:**

1. **Round-robin:** Each agent takes turns in a fixed sequence, regardless of context.
2. **Role-based:** The next speaker is chosen based on predefined roles or expertise (e.g., technical expert, project manager).
3. **Trigger-based:** Specific keywords, intents, or actions trigger a handoff to a particular agent.
4. **Context-aware:** The system analyzes conversation context, history, and goals to dynamically select the most appropriate agent.
5. **Manual override:** A user or supervisor explicitly selects the next speaker.

**Transitions:**

- **Handoff:** An agent passes control to another agent, often mid-task. Useful for dividing complex workflows.
- **After work:** An agent provides a summary, validation, or follow-up after another agent completes their part.

---

## Examples

### Example 1: Round-robin Selection

```python
agents = [agent1, agent2, agent3]
current_speaker_idx = 0

def select_next_speaker():
    global current_speaker_idx
    speaker = agents[current_speaker_idx]
    current_speaker_idx = (current_speaker_idx + 1) % len(agents)
    return speaker
```

### Example 2: Role-based Handoff

```python
def select_speaker(intent):
    if intent == "technical_question":
        return technical_expert_agent
    elif intent == "project_update":
        return project_manager_agent
    else:
        return default_agent
```

### Example 3: Context-aware After Work Transition

```python
def after_work_transition(last_agent, conversation_history):
    if last_agent == data_gatherer_agent:
        return summarizer_agent  # Summarizer provides a summary after data gathering
    return None
```

### Example 4: Custom Orchestration with Dynamic Selection

```python
def select_next_speaker(conversation_state):
    if conversation_state["requires_approval"]:
        return supervisor_agent
    elif conversation_state["task"] == "coding":
        return developer_agent
    elif conversation_state["last_agent"] == developer_agent:
        return reviewer_agent  # After work transition
    else:
        return default_agent
```

---

## Best Practices

- **Align speaker selection with task roles:** Ensure agents are mapped to tasks that match their expertise.
- **Design clear handoff criteria:** Avoid ambiguity in when and how handoffs occur.
- **Preserve conversation context:** Carry relevant state and history during transitions.
- **Provide fallback logic:** Handle unexpected inputs or scenarios gracefully.
- **Monitor and log transitions:** For debugging and improving orchestration patterns.
- **Facilitate manual override:** Allow human intervention when necessary.
- **Test with realistic workflows:** Simulate multi-turn, multi-agent interactions to validate orchestration logic.

**Common Pitfalls:**

- Rigid speaker selection leading to unnatural conversations.
- Unclear handoff points causing confusion or dropped tasks.
- Losing context during after work transitions.
- Overcomplicating selection logic, making the system hard to maintain.

---

## Related Concepts

- [Agent orchestration patterns](./agent-orchestration-patterns.md)
- [LLM configuration and model clients](./llm-configuration.md)
- [Task routing strategies](./task-routing.md)
- [Conversation state management](./conversation-state.md)
- [Human-in-the-loop orchestration](./human-in-the-loop.md)
- [Handoff and after work transitions](./handoff-and-afterwork.md)

For a deeper dive on orchestration and advanced agent design, see [Multi-Agent Collaboration Patterns](./multi-agent-collaboration.md).