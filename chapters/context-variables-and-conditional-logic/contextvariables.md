# Context Variables

## Overview

**Context Variables** are dynamic data elements used to store and share information throughout a multi-agent workflow. They enable agents to pass information, remember state, and make decisions based on previous outcomes. In advanced agent orchestration, context variables are crucial for enabling conditional logic, context-aware transitions, and complex flow control across different agents and workflow stages.

## Explanation

Context variables act as a shared memory for agents working in a coordinated workflow. Each agent can read from, write to, or update these variables as tasks progress. This allows for:

- **State Persistence:** Agents can reference what has happened previously.
- **Dynamic Decision Making:** Flows can branch or loop based on context.
- **Data Passing:** Outputs from one agent can be inputs to another.

### How Context Variables Work

1. **Initialization:** Variables are set at the start of the workflow or dynamically during execution.
2. **Access and Modification:** Any agent in the workflow can read or update context variables.
3. **Conditional Logic:** Transitions between agents or workflow branches can use expressions evaluating context variables.

### Example Use Cases

- Track user preferences or session data.
- Store results from API calls for later use.
- Decide next agent or action based on status codes or flags.

## Examples

### 1. Storing and Updating Variables

```yaml
# YAML-like workflow definition
context:
  user_name: null
  order_status: null

agents:
  - id: get_user_info
    action: fetch_user
    on_complete:
      set:
        user_name: $result.name

  - id: process_order
    action: process_order
    on_complete:
      set:
        order_status: $result.status
```

### 2. Conditional Logic for Transitions

```yaml
transitions:
  - from: process_order
    to: notify_success
    condition: context.order_status == "success"

  - from: process_order
    to: notify_failure
    condition: context.order_status != "success"
```

In this example, the workflow checks the `order_status` context variable to determine which notification agent to run.

### 3. Context Expressions for Complex Flow Control

```yaml
# Pseudocode for an agent decision block
if context.user_type == 'admin' and context.request_priority > 5:
    next_agent = 'priority_handler'
else:
    next_agent = 'standard_handler'
```

## Best Practices

- **Initialize Variables:** Always define context variables before use to avoid undefined errors.
- **Use Clear Naming:** Name variables descriptively to avoid confusion and conflicts.
- **Limit Scope:** Store only necessary data in context to keep workflows efficient.
- **Update Thoughtfully:** Avoid unnecessary overwrites; preserve important historical context.
- **Validate Before Use:** Check for null or unexpected values before branching logic.
- **Keep Expressions Simple:** Complex expressions can be hard to debug—break them into multiple steps if possible.

## Related Concepts

- [Conditional Logic](./ConditionalLogic.html)
- [Agent Transitions](./AgentTransitions.html)
- [Context Expressions](./ContextExpressions.html)
- [State Management in Multi-Agent Systems](./StateManagement.html)
- [Advanced Agent Orchestration](./AdvancedAgentOrchestration.html)

**Further Reading:**  
- [OpenAI Cookbook: Orchestrating Multi-Agent Workflows](https://github.com/openai/openai-cookbook)
- [Workflow Patterns for Context Management](https://www.workflowpatterns.com/patterns/control/)

---

By mastering context variables, you enable sophisticated, adaptive, and efficient multi-agent workflows. Proper use of context and conditional logic is foundational for advanced orchestration and intelligent agent design.