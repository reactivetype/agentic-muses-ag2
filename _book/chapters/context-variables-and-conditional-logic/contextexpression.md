# ContextExpression

## Overview

A **ContextExpression** is a feature in advanced agent orchestration that allows workflows to dynamically reference, evaluate, and manipulate context variables. These expressions empower agents to make decisions, branch logic, and share data across complex, multi-agent environments. By leveraging context expressions, orchestrators can implement conditional logic, update state, and control agent transitions based on evolving workflow data.

---

## Explanation

Context variables act as shared memory in agent orchestration, holding information such as user inputs, intermediate results, and agent states. **ContextExpressions** are mechanisms to evaluate and manipulate these variables using expressions embedded within the workflow configuration.

A ContextExpression can:

- **Read** values stored in the context (e.g., `context.user_name`)
- **Write or update** context variables (e.g., `context.task_status = "done"`)
- **Evaluate conditions** for flow control (e.g., `context.score > 80`)
- **Combine logic** using operators (e.g., `context.flagA && !context.flagB`)
- **Support templating** for dynamic message generation (e.g., `"Hello, ${context.user_name}!"`)

ContextExpressions are typically used in:

- **Agent transition conditions**: Deciding which agent to activate next.
- **Task completion checks**: Verifying if an agent’s goal is achieved.
- **Dynamic prompt construction**: Personalizing instructions or responses.
- **Branching and looping**: Implementing complex flows based on context.

### Syntax

Most ContextExpressions use a subset of JavaScript or Python-like syntax, depending on the orchestration platform. They support:

- References to context variables: `context.variableName`
- Standard logical (`&&`, `||`, `!`) and comparison (`==`, `!=`, `<`, `>`, etc.) operators
- String interpolation/templating
- Function calls (if supported by the platform)

---

## Examples

### 1. Conditional Agent Transition

```yaml
transitions:
  - condition: context.user_authenticated == true
    target_agent: "DataRetrievalAgent"
  - condition: context.auth_attempts > 3
    target_agent: "LockoutAgent"
```

### 2. Updating Context Variables

```python
# Python-like pseudocode in an agent step
if task_complete:
    context["task_status"] = "done"
else:
    context["task_status"] = "pending"
```

### 3. Dynamic Prompt Construction

```yaml
prompt: "Welcome, ${context.user_name}. Your current balance is $${context.balance}."
```

### 4. Complex Flow Control

```yaml
if: context.user_role == "admin" && context.requested_action == "shutdown"
then:
  next_agent: "AdminApprovalAgent"
else:
  next_agent: "StandardWorkflowAgent"
```

### 5. Looping Until Condition Met

```yaml
while: context.retry_count < 3 && context.success == false
do:
  agent: "RetryAgent"
```

---

## Best Practices

- **Initialize context variables** before use to avoid undefined errors.
- **Use descriptive variable names** to improve maintainability.
- **Document complex ContextExpressions** inline for clarity.
- **Avoid deeply nested logic** in expressions—refactor into discrete steps if possible.
- **Validate expressions** for syntactic and logical errors (use built-in validators if available).
- **Keep logic deterministic**; avoid side effects inside expressions.
- **Handle missing or null values** gracefully (e.g., `context.value ?? default_value`).

**Common Pitfalls:**

- Forgetting to update context variables after agent actions.
- Using platform-specific syntax inconsistently (e.g., mixing Python and JavaScript styles).
- Overloading expressions with too much logic, making them hard to debug.

---

## Related Concepts

- [Context Variables](#)  
- [Conditional Logic in Workflows](#)  
- [Agent Transition Rules](#)  
- [Data Passing Between Agents](#)  
- [Templating and String Interpolation](#)  
- [Advanced Agent Orchestration](#)  

For further reading, consult the documentation for your orchestration platform on [flow control mechanisms](#) and [context management best practices](#).

---