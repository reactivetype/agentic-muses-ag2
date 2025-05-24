# OnCondition and nested chat transitions

## Overview

In advanced agent orchestration, group and swarm workflows often require dynamic, context-sensitive transitions. **OnCondition** and **nested chat transitions** are core patterns that enable agents to react to runtime conditions and orchestrate complex, multi-step conversations. By leveraging these patterns—especially in conjunction with constructs like `AfterWork`—developers can design scalable agent collectives that adapt to evolving task states and collaborative needs.

---

## Explanation

### OnCondition

**OnCondition** is a workflow construct that allows agents or groups to **conditionally trigger transitions** or actions based on runtime predicates. This enables orchestration logic such as:

- Branching workflows according to agent results
- Coordinating multiple agents based on shared state
- Reacting to failures, successes, or specific data

In group and swarm settings, **OnCondition** is often used to synchronize progress or trigger collective responses.

#### Syntax Example

```python
OnCondition(predicate, then=transition)
```
- `predicate`: A function or expression evaluated in the current workflow context.
- `then`: The transition or action to perform if the predicate is true.

### Nested Chat Transitions

**Chat transitions** represent conversational state changes between agents or groups. **Nested** transitions occur when a transition triggers another chat or agent workflow, allowing for:

- Multi-level agent delegation
- Subtask orchestration within group or swarm patterns
- Layered escalation or fallback behaviors

#### AfterWork

The **AfterWork** construct is commonly used to chain transitions after an agent (or group) completes its assigned work. Combining `OnCondition` with `AfterWork` enables highly dynamic, reactive agent orchestration.

#### Example Flow

1. Group of agents completes initial work.
2. `AfterWork` triggers an `OnCondition` check.
3. If the condition is met, a nested chat or agent workflow is launched.

---

## Examples

### Example 1: Swarm Review with Conditional Rework

Suppose a swarm of agents reviews a document. If any agent flags an issue, a nested chat is started to resolve it.

```python
# Pseudocode for clarity

# Swarm group reviews a document
swarm = SwarmAgentGroup(
    agents=[ReviewerAgent1(), ReviewerAgent2(), ReviewerAgent3()],
    task=ReviewDocumentTask(document)
)

# After all reviewers complete, check if any issues were flagged
AfterWork(
    swarm,
    OnCondition(
        predicate=lambda ctx: any(r.issues for r in ctx.results),
        then=NestedChat(
            agents=[LeadReviewer()],
            task=ResolveIssuesTask(ctx.collect_issues())
        )
    )
)
```
**Explanation:**  
- The swarm reviews the document in parallel.
- After all reviews, `OnCondition` checks if there are issues.
- If so, a nested chat with a lead reviewer is triggered.

---

### Example 2: Group Escalation on Failure

If a set of agents fails to reach consensus, escalate to a supervisor agent.

```python
group = AgentGroup(
    agents=[AgentA(), AgentB()],
    task=DecisionTask()
)

AfterWork(
    group,
    OnCondition(
        predicate=lambda ctx: not ctx.result.consensus,
        then=NestedChat(
            agents=[SupervisorAgent()],
            task=ResolveDisagreementTask(ctx.result.details)
        )
    )
)
```
**Explanation:**  
- Initial agents attempt to reach consensus.
- If failed, escalation is automatically triggered via a nested chat.

---

### Example 3: Multi-level Delegation

A primary agent delegates a task to a group. If the group cannot handle it, the task is escalated to a swarm.

```python
primary_agent = PrimaryAgent()

AfterWork(
    primary_agent,
    OnCondition(
        predicate=lambda ctx: ctx.result.status == 'needs_help',
        then=NestedChat(
            agents=[HelperGroup()],
            task=AssistTask(ctx.result.details),
            after=OnCondition(
                predicate=lambda ctx: ctx.result.status == 'unresolved',
                then=NestedChat(
                    agents=[Swarm()],
                    task=EscalatedAssistTask(ctx.result.details)
                )
            )
        )
    )
)
```
**Explanation:**  
- Nested transitions allow fallback to increasingly capable groups.

---

## Best Practices

- **Keep predicates simple and performant:**  
  Complex conditions can slow orchestration or introduce hard-to-debug logic.

- **Avoid deep nesting:**  
  Excessive nested transitions can make workflows hard to follow and maintain.  
  Use clear hierarchy and documentation.

- **Leverage shared context:**  
  Ensure all nested transitions receive the necessary context or results from parent workflows.

- **Plan for failure and timeouts:**  
  Always handle error conditions and consider what happens if nested chats do not resolve as expected.

- **Test at each orchestration level:**  
  Unit test each OnCondition and AfterWork transition independently before integrating.

---

## Related Concepts

- [Agent Group Patterns](agent-group-patterns.md)
- [Swarm Coordination Strategies](swarm-coordination.md)
- [Agent Capabilities and Composability](agent-capabilities.md)
- [Advanced Agent Orchestration](advanced-agent-orchestration.md)
- [Error Handling and Recovery in Agent Workflows](error-handling-in-agents.md)
- [Composable Agent Workflows](composable-agent-workflows.md)

---

For further reading, see the documentation on [Nested Transitions](nested-transitions.md) and [AfterWork Patterns](afterwork-patterns.md).