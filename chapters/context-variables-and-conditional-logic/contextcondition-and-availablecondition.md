# ContextCondition and AvailableCondition

## Overview

In advanced agent orchestration, **context variables** are key-value pairs that persist and evolve throughout a multi-agent workflow. They enable agents to share state and make dynamic decisions. **ContextCondition** and **AvailableCondition** are mechanisms that leverage these variables to introduce conditional logic—controlling agent transitions, task execution, and workflow paths based on current context.

**ContextCondition** evaluates boolean expressions against the context, determining whether certain actions or transitions should proceed. **AvailableCondition** is a specialized form used to control agent or tool availability based on context.

---

## Explanation

### Context Variables

Context variables are shared data accessible to all agents within a workflow. They are typically updated as agents execute tasks, enabling downstream agents to react to prior outcomes.

### ContextCondition

A **ContextCondition** is an expression that references one or more context variables, evaluated at runtime. It is used to:

- Gate agent transitions (e.g., only proceed if `task_completed == true`)
- Trigger specific actions based on workflow state
- Implement branching and loop logic

**Syntax:**  
ContextCondition expressions are usually written in a domain-specific language or Python-like syntax, referencing context variables directly.

**Example:**
```yaml
condition: context['user_verified'] == True and context['attempts'] < 3
```

### AvailableCondition

An **AvailableCondition** determines whether a particular agent, tool, or resource should be considered "available" for selection or execution, based on the current context.

**Example:**
```yaml
available_condition: context.get('document_uploaded', False)
```
This would make the agent available only if a document has been uploaded.

### Evaluating Conditions

Both ContextCondition and AvailableCondition are evaluated against the current state of the context. If the condition evaluates to `True`, the associated transition, action, or agent becomes eligible for execution.

---

## Examples

### Example 1: Agent Transition with ContextCondition

```yaml
agents:
  - name: VerificationAgent
    on_success:
      target: ProcessAgent
      condition: context['user_verified'] == True
    on_failure:
      target: RetryAgent
      condition: context['attempts'] < 3
```
**Explanation:**  
- The transition to `ProcessAgent` only occurs if the context variable `user_verified` is `True`.
- If not, and if `attempts` is less than 3, the workflow transitions to `RetryAgent`.

---

### Example 2: Tool Availability with AvailableCondition

```yaml
tools:
  - name: Summarizer
    available_condition: context.get('input_ready', False)
```
**Explanation:**  
- The `Summarizer` tool is only available if the context variable `input_ready` is `True`.

---

### Example 3: Dynamic Branching

```python
if context['score'] > 80:
    next_agent = 'HighPerformerAgent'
elif context['score'] > 50:
    next_agent = 'AveragePerformerAgent'
else:
    next_agent = 'NeedsImprovementAgent'
```
**Explanation:**  
- The workflow dynamically routes to a different agent depending on the `score` context variable.

---

## Best Practices

- **Initialize Context Variables:** Ensure all required context variables are initialized before evaluation to avoid runtime errors.
- **Keep Conditions Simple:** Write clear, concise conditions to maintain readability and ease debugging.
- **Centralize Context Updates:** Update context variables in predictable locations (e.g., agent completion hooks) to prevent race conditions.
- **Use Default Values:** When accessing context variables, use `.get()` with defaults to handle missing keys gracefully.
- **Test Complex Logic:** For intricate conditions, unit test expressions independently to ensure correct evaluation.
- **Document Variable Usage:** Clearly document which agents update or depend on which context variables.

**Common Pitfalls:**
- Using undefined context variables, leading to errors
- Overly complex expressions, making the workflow hard to maintain
- Accidental overwriting of context keys by multiple agents

---

## Related Concepts

- [Context Variables](#)  
- [Agent Transitions](#)  
- [Conditional Branching](#)  
- [Multi-Agent Workflow Patterns](#)  
- [Error Handling in Agent Orchestration](#)  
- [Advanced Control Flow Expressions](#)

For further reading, consult your orchestration platform's documentation on [conditional logic](#) and [context management](#).