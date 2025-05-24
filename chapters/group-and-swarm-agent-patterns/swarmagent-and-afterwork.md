# SwarmAgent and AfterWork

## Overview

**SwarmAgent** and **AfterWork** are advanced orchestration patterns used for managing groups of agents in scalable, dynamic workflows. These constructs enable the coordination of multiple agents—either working in parallel ("swarm") or in nested, sequential flows ("after work")—to solve complex tasks. They are essential for building flexible systems where agent capabilities are composed and orchestrated based on runtime conditions, enabling both reactive and proactive behavior in multi-agent environments.

---

## Explanation

### SwarmAgent

A **SwarmAgent** is a controller or orchestrator that manages a set of agents working in parallel or semi-parallel fashion toward a collective goal. Swarm patterns are well-suited for tasks that benefit from diversity, redundancy, or collaborative problem-solving, where agents operate independently but their outputs are collectively synthesized.

**Key Features:**
- **Parallel Execution:** Agents in the swarm can act simultaneously, reducing overall latency.
- **Aggregation:** SwarmAgent collects and aggregates results from its members.
- **Dynamic Membership:** Swarm composition can change at runtime based on context or conditions.

### AfterWork

**AfterWork** is a workflow modifier that introduces follow-up processing after the main agent or group completes its task. This is especially useful for **nested chat transitions**, where the output of one agent triggers further processing by another agent or group, enabling stepwise refinement or layered reasoning.

**Key Features:**
- **Chaining:** Output from one agent or group seamlessly becomes input for another.
- **Nested Workflows:** Enables composition of complex, multi-step agent flows.
- **Stateful Transitions:** Preserves context across transitions.

### OnCondition

**OnCondition** is an orchestration pattern used to route control or data to different agents or groups based on the evaluation of runtime conditions. It allows for the implementation of flexible decision logic within SwarmAgent or AfterWork workflows.

---

## Examples

### 1. SwarmAgent with Parallel Agents

```python
from agents.swarm import SwarmAgent

# Define agents
class WebScraperAgent(Agent): ...
class DataExtractorAgent(Agent): ...
class SentimentAnalyzerAgent(Agent): ...

# Swarm Agent orchestrates parallel execution
swarm = SwarmAgent([
    WebScraperAgent(),
    DataExtractorAgent(),
    SentimentAnalyzerAgent()
])

results = swarm.run(input_data)
# Aggregated results from all agents
```

### 2. AfterWork for Nested Chat Transitions

```python
from agents.workflow import AfterWork

# Define initial and follow-up agents
class QuestionAnsweringAgent(Agent): ...
class ExplanationAgent(Agent): ...

# Chain agents: first answer, then explain
qa_with_explanation = AfterWork(
    QuestionAnsweringAgent(),
    ExplanationAgent()
)

final_response = qa_with_explanation.run(user_query)
# Output: Answer with detailed explanation
```

### 3. SwarmAgent with OnCondition

```python
from agents.control import OnCondition

def is_urgent(input_data):
    return 'urgent' in input_data['tags']

urgent_agent = FastResponseAgent()
default_agent = StandardResponseAgent()

decision_agent = OnCondition(
    condition=is_urgent,
    if_true=urgent_agent,
    if_false=default_agent
)

# Embed in a Swarm for dynamic routing
swarm = SwarmAgent([
    decision_agent,
    LoggingAgent()
])

swarm.run(input_data)
```

---

## Best Practices

- **Design for Idempotency:** Ensure agents in a swarm can be run independently; avoid side effects that interfere with other agents.
- **Aggregate Results Thoughtfully:** Use reduction or voting strategies to synthesize swarm outputs.
- **Guard Against Race Conditions:** When agents modify shared state, use synchronization mechanisms.
- **Limit Depth of AfterWork Chains:** Excessive nesting can make debugging and tracing harder.
- **Use OnCondition for Clear Routing:** Centralize decision logic for maintainability and clarity.
- **Monitor and Log Execution:** Instrument swarm and afterwork flows to capture performance and failures.

**Common Pitfalls:**
- Over-complicating orchestration logic, leading to hard-to-maintain workflows.
- Failing to handle partial failures in swarms, causing silent data loss.
- Allowing unchecked nesting in AfterWork, resulting in stack overflows or excessive resource usage.

---

## Related Concepts

- [Agent Composability](./agent-composability.md)
- [Advanced Agent Orchestration](./advanced-agent-orchestration.md)
- [OnCondition Pattern](./oncondition-pattern.md)
- [Agent Capabilities](./agent-capabilities.md)
- [Workflow Modifiers](./workflow-modifiers.md)
- [Fault Tolerance in Multi-Agent Systems](./fault-tolerance.md)
- [Monitoring and Logging in Agent Systems](./monitoring-logging.md)

For further reading, see:
- [Swarm Intelligence: Principles, Advances, and Applications](https://en.wikipedia.org/wiki/Swarm_intelligence)
- [Nested Workflows in Agent-Oriented Programming](https://www.sciencedirect.com/science/article/pii/S0957417419304575)