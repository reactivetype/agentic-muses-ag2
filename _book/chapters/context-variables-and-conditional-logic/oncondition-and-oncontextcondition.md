# OnCondition and OnContextCondition

## Overview

In advanced agent orchestration, **OnCondition** and **OnContextCondition** are mechanisms that enable dynamic, context-aware transitions between agents or workflow steps. They allow you to encode conditional logic that evaluates context variables and determines agent behavior or routing within a multi-agent system. By leveraging these constructs, orchestration can adapt to changing context, user input, or external signals, enabling more flexible and intelligent workflows.

---

## Explanation

**OnCondition** and **OnContextCondition** are used to control the flow of execution in multi-agent workflows based on evaluated conditions:

- **OnCondition**: Triggers a transition or action when a specified boolean expression or condition is met. The condition may reference current context variables, agent states, or external inputs.
- **OnContextCondition**: Similar to OnCondition, but specifically focuses on expressions that involve context variables, such as user state, workflow progress, or shared memory between agents.

**Context variables** are key-value pairs stored in a workflow's context object. They allow agents to share information, track progress, or store temporary results. By updating and evaluating these variables, agents can influence each other's behavior and orchestrate complex, adaptive flows.

### How it Works

1. **Storing Context Variables**: Agents or orchestrators set and update context variables during execution.
2. **Defining Conditions**: Conditions are expressed using a supported expression language (e.g., Python, Jinja, JSONata, or custom DSL).
3. **Evaluating Conditions**: The orchestrator evaluates the condition at runtime; if it returns `true`, the specified transition or action is executed.
4. **Flow Control**: This enables branching, looping, or early exits from workflows, depending on context.

---

## Examples

### Example 1: Conditional Agent Routing

```yaml
# Pseudocode for a workflow definition
steps:
  - id: gather_user_info
    agent: UserInfoAgent
    on_complete:
      - action: set_context
        key: user_age
        value: "{{ output.age }}"
      - action: go_to
        step: age_check

  - id: age_check
    on_context_condition:
      condition: "{{ context.user_age >= 18 }}"
      next_step: adult_flow
    else:
      next_step: minor_flow

  - id: adult_flow
    agent: AdultServicesAgent
    ...

  - id: minor_flow
    agent: MinorServicesAgent
    ...
```

**Explanation:**  
- After gathering user info, the workflow stores the user's age in a context variable.
- `on_context_condition` checks the age and routes the flow to either `adult_flow` or `minor_flow` accordingly.

---

### Example 2: Looping Until a Condition is Met

```python
# Pseudocode for an agent loop using OnCondition

while not context["done"]:
    agent_output = SomeAgent.act(context)
    context["done"] = agent_output["is_complete"]
    if context["done"]:
        break
```

**Explanation:**  
- The agent continues to run until the `"done"` context variable is set to `True` by agent output.

---

### Example 3: Using OnCondition for Error Handling

```yaml
- id: process_payment
  agent: PaymentAgent
  on_condition:
    condition: "{{ output.success == false }}"
    next_step: handle_payment_error
  else:
    next_step: confirm_order
```

**Explanation:**  
- If payment fails (`output.success == false`), the workflow transitions to an error handler; otherwise, it confirms the order.

---

## Best Practices

- **Keep Conditions Simple:** Complex logic can become hard to maintain; try to encapsulate logic in well-named context variables.
- **Type Safety:** Ensure context variables are properly typed and initialized to avoid runtime errors.
- **Document Context Usage:** Clearly document which agents set, read, or modify specific context variables.
- **Avoid Circular Dependencies:** Be careful when agents depend on variables set by others in the same step or cycle.
- **Test Conditions:** Write tests for branching logic to ensure all paths are covered and conditions behave as expected.
- **Graceful Failure:** Always provide fallback paths (e.g., `else` branches) for conditions that may not be met.

---

## Related Concepts

- [Context Variables](./context-variables.html)
- [Agent Transition Management](./agent-transitions.html)
- [Expression Languages for Orchestration](./expression-languages.html)
- [Error Handling in Workflows](./error-handling.html)
- [Advanced Agent Orchestration (Prerequisite)](./advanced-agent-orchestration.html)
- [Looping and Iterative Flows](./looping-and-iteration.html)

For more information on multi-agent workflows, see [Multi-Agent Workflows](./multi-agent-workflows.html).