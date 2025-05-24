# Pattern classes for orchestration

## Overview

Pattern classes for orchestration are modular constructs that enable advanced coordination of multiple agents in group or swarm settings. These patterns abstract common orchestration strategies such as task distribution, conditional execution, and workflow transitions, providing reusable mechanisms for building scalable and flexible multi-agent systems. By leveraging these patterns—such as `AfterWork`, `OnCondition`, and others—developers can efficiently manage agent collaboration, ensure robust communication, and design workflows that dynamically adapt to the environment or task outcomes.

---

## Explanation

### 1. Group and Swarm Patterns

- **Group patterns** focus on orchestrating a fixed or structured collection of agents, often with explicit roles or responsibilities.
- **Swarm patterns** emphasize decentralized coordination, where agents operate with collective, emergent behaviors and minimal central control.

Pattern classes encapsulate complex orchestration logic, making it easier to compose, extend, and maintain group or swarm workflows.

### 2. Key Pattern Classes

#### `AfterWork`

`AfterWork` handles workflow transitions by specifying what should occur after a set of agents (or a group) completes their current work. It's instrumental in defining nested chat transitions or follow-up tasks, enabling seamless chaining and coordination of agent activities.

**Usage:**
- Triggering a follow-up discussion or review after task completion
- Routing outputs to subsequent workflows or agent groups

#### `OnCondition`

`OnCondition` enables conditional orchestration based on the state of agents, their outputs, or environmental cues. It supports designing complex, adaptive workflows that respond to dynamic conditions.

**Usage:**
- Branching workflows depending on results or agent feedback
- Triggering escalation or fallback procedures

### 3. Orchestration Patterns in Action

By combining these pattern classes, developers can build nested, adaptive workflows, such as:
- A swarm of agents collaboratively analyzing data, with a group leader initiating a summary phase (`AfterWork`) once consensus is reached.
- Conditional escalation to an expert group (`OnCondition`) if swarm confidence is low.

---

## Examples

### Example 1: Nested Chat Transitions with `AfterWork`

```python
from orchestration.patterns import AfterWork, Group, Agent

# Define agents
reviewers = Group([Agent("Reviewer1"), Agent("Reviewer2")])
moderator = Agent("Moderator")

# Workflow: Reviewers discuss, then moderator summarizes
workflow = AfterWork(
    group=reviewers,
    after=lambda outputs: moderator.chat(inputs=outputs)
)

result = workflow.run(inputs="Review this document.")
```
*In this example, the `AfterWork` pattern transitions from a group discussion to a moderator summary phase.*

---

### Example 2: Conditional Escalation with `OnCondition`

```python
from orchestration.patterns import OnCondition, Swarm, Agent

# Swarm of agents analyzing a dataset
analysts = Swarm([Agent("AnalystA"), Agent("AnalystB"), Agent("AnalystC")])
expert = Agent("Expert")

# Condition: Escalate if consensus score < threshold
def low_confidence(context):
    return context['consensus_score'] < 0.7

workflow = OnCondition(
    condition=low_confidence,
    if_true=lambda context: expert.chat(inputs=context['analysis']),
    if_false=lambda context: context['analysis']
)

# Compose with main analysis swarm
outputs = analysts.run(inputs="Analyze this data.")
result = workflow.run(context={'consensus_score': outputs.score, 'analysis': outputs.data})
```
*Here, `OnCondition` directs the workflow based on swarm consensus.*

---

### Example 3: Combining Patterns for Complex Orchestration

```python
# Swarm collaborates, then conditional follow-up with expert group
swarm = Swarm([...])
experts = Group([...])

def needs_expert_review(context):
    return context['flagged']

main_workflow = AfterWork(
    group=swarm,
    after=lambda outputs: OnCondition(
        condition=needs_expert_review,
        if_true=lambda context: experts.chat(inputs=context['outputs']),
        if_false=lambda context: context['outputs']
    ).run(context={'flagged': outputs.flagged, 'outputs': outputs.data})
)

final_result = main_workflow.run(inputs="Process this request.")
```
*This pattern chains `AfterWork` and `OnCondition` for robust multi-stage workflows.*

---

## Best Practices

- **Encapsulate orchestration logic:** Use pattern classes to isolate workflow logic from agent implementation.
- **Promote composability:** Chain pattern classes to build complex workflows from simple primitives.
- **Design for scalability:** Use swarm patterns for large, decentralized agent sets; group patterns for structured collaboration.
- **Leverage conditions wisely:** Ensure `OnCondition` triggers are explicit and based on well-defined agent outputs or states.
- **Handle nested transitions:** Use `AfterWork` to manage multi-stage workflows and avoid tangled control flows.
- **Monitor for deadlocks:** Avoid circular transitions or unhandled conditions that can stall workflows.

---

## Related Concepts

- [Advanced Agent Orchestration](#)
- [Agent Capabilities and Composability](#)
- [Swarm Intelligence](#)
- [Agent Roles and Group Dynamics](#)
- [Workflow Composition Patterns](#)
- [Conditional Logic in Multi-Agent Systems](#)
- [Event-Driven Orchestration](#)

---

For further reading, see the documentation on [Group and Swarm Agent Patterns](#) and [Composable Agent Architectures](#).