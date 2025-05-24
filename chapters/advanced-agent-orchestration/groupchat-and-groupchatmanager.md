# GroupChat and GroupChatManager

## Overview

**GroupChat** and **GroupChatManager** are advanced abstractions for orchestrating multiple agents in collaborative conversational workflows. They enable you to coordinate interactions among multiple language model agents within a single conversation, supporting complex patterns such as multi-agent discussions, dynamic speaker selection, and intelligent handoffs. These constructs are essential for building robust, multi-faceted AI systems where agents with different roles and expertise work together toward a shared goal.

---

## Explanation

### What is GroupChat?

A **GroupChat** is a structured conversation involving multiple agents (LLMs or tool-augmented agents). Unlike a single-agent chat, GroupChat manages the flow of messages, tracks speaker turns, and maintains conversation state across agents. It enables orchestration patterns such as round-robin discussion, expert handoff, and consensus building.

### What is GroupChatManager?

The **GroupChatManager** acts as the conductor of the GroupChat. It controls which agent should speak next, manages transitions (including handoffs and after-work transitions), and enforces orchestration policies. The manager can be customized to implement various decision logic for speaker selection and agent transitions based on context, agent capabilities, or conversation history.

### Key Features

- **Speaker Selection:** Dynamically choose which agent responds at each turn based on context or predefined rules.
- **Agent Transitions:** Seamlessly transition between agents, allowing for task-specific handoff or multi-step collaboration.
- **Orchestration Patterns:** Implement patterns such as round-robin, expert-in-the-loop, or conditional delegation.
- **State Management:** Maintain shared context and message history across all agents in the group.

---

## Examples

### 1. Basic GroupChat Setup

Let's set up a basic GroupChat where two agents collaborate to answer user questions.

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain_experimental.agents import GroupChat, GroupChatManager
from langchain_openai import ChatOpenAI

# Define two agents with different expertise
support_agent = create_openai_functions_agent(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    tools=[],  # Add support tools here
    prompt=ChatPromptTemplate.from_template("You are a customer support agent.")
)

expert_agent = create_openai_functions_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=[],  # Add expert tools here
    prompt=ChatPromptTemplate.from_template("You are a technical expert.")
)

# Wrap agents as executors
support_executor = AgentExecutor(agent=support_agent, tools=[])
expert_executor = AgentExecutor(agent=expert_agent, tools=[])

# Create the GroupChat
group_chat = GroupChat(
    agents=[support_executor, expert_executor],
    messages=[],
    max_rounds=5
)

# Create a GroupChatManager
manager = GroupChatManager(groupchat=group_chat)

# Run the group chat
result = manager.run(input="How can I reset my device password?")
print(result)
```

### 2. Custom Speaker Selection

Customize which agent should respond based on message content.

```python
class CustomGroupChatManager(GroupChatManager):
    def select_speaker(self, message):
        if "technical" in message.content.lower():
            return self.groupchat.agents[1]  # expert_agent
        else:
            return self.groupchat.agents[0]  # support_agent

manager = CustomGroupChatManager(groupchat=group_chat)
```

### 3. Agent Handoff Example

Implement a handoff: after the support agent gathers details, the expert agent takes over.

```python
class HandoffGroupChatManager(GroupChatManager):
    def select_speaker(self, message):
        if "need technical assistance" in message.content.lower():
            return self.groupchat.agents[1]  # expert_agent
        else:
            return self.groupchat.agents[0]  # support_agent

    def after_work(self, last_speaker, message):
        # Optionally notify agents or log handoffs
        pass

manager = HandoffGroupChatManager(groupchat=group_chat)
```

---

## Best Practices

- **Define Clear Agent Roles:** Clearly specify each agent’s expertise and responsibilities to avoid redundant or conflicting responses.
- **Customize Speaker Logic:** Tailor the `select_speaker` logic to match your application's needs, such as keyword triggers, user roles, or agent confidence.
- **Limit Rounds:** Set a sensible `max_rounds` to prevent infinite loops and improve efficiency.
- **Handle Handoffs Gracefully:** Ensure context is passed cleanly between agents during transitions for seamless user experience.
- **Monitor and Log Transitions:** Track which agent handles each turn for transparency and debugging.
- **Manage Shared State:** Use a consistent state or memory object to maintain context across agents.
- **Test with Realistic Scenarios:** Simulate group chat flows to identify edge cases or breakdowns in orchestration.

### Common Pitfalls

- **Uncontrolled Loops:** Failing to limit conversation rounds can lead to runaway discussions.
- **Ambiguous Agent Roles:** Overlapping agent responsibilities can confuse both agents and users.
- **Loss of Context:** Not synchronizing shared memory/context may cause agents to miss important details.
- **Hardcoded Transitions:** Rigid `select_speaker` logic can make the system inflexible; consider data-driven approaches when possible.

---

## Related Concepts

- [LLM Configuration and Model Clients](./llm-configuration.md)
- [Tool-augmented Agents](./tool-augmented-agents.md)
- [AgentExecutor](./agent-executor.md)
- [Prompt Engineering](./prompt-engineering.md)
- [Multi-Agent Collaboration Patterns](https://python.langchain.com/docs/agents/multi_agent)
- [State Management and Memory](./state-management.md)
- [LangChain Experimental Agents Documentation](https://python.langchain.com/docs/experimental/groupchat/)

---

By leveraging **GroupChat** and **GroupChatManager**, you can orchestrate complex, multi-agent conversations, enabling collaborative intelligence and richer user experiences in your AI applications.