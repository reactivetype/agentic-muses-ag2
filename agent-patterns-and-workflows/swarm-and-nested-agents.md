# Swarm and Nested Agents


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Accuracy and Technical Correctness"
      description: "Some code snippets use ellipses {...} or undefined variables (e.g., agent_a, agent_b) which are placeholders and may confuse users or cause errors if copied directly."
      severity: "medium"
      suggestion: "Provide concrete, minimal working code for all examples or clearly note where placeholders should be replaced."
    - type: "Clarity and Readability"
      description: "Dense explanations and technical jargon (e.g., 'encapsulate', 'abstractions', 'transition logic') may be challenging for less advanced users."
      severity: "low"
      suggestion: "Simplify language where possible, add diagrams or more inline comments to explain complex concepts."
    - type: "Completeness and Comprehensiveness"
      description: "While the section is comprehensive, it lacks explicit discussion of potential pitfalls, limitations, or troubleshooting tips for swarms/nested agents (e.g., deadlocks, race conditions)."
      severity: "medium"
      suggestion: "Add a brief subsection or note on known limitations, common issues, and how to mitigate them."
    - type: "Code Example Quality"
      description: "The 'Conditional Agent Handoff with OnCondition' example uses undefined agents and could be confusing. Also, some code lacks context (imports, LLM config, agent instantiation)."
      severity: "medium"
      suggestion: "Ensure all code examples are self-contained, runnable, and include necessary context or setup."
    - type: "Best Practices Coverage"
      description: "Best practices are generally strong but could benefit from examples or links to further resources for each point."
      severity: "low"
      suggestion: "Provide code snippets or links to documentation/examples for each best practice, where appropriate."
  strengths:
    - "Comprehensive coverage of swarm and nested agent patterns, including advanced orchestration and transition mechanisms."
    - "Provides practical, scenario-driven code examples illustrating key concepts."
    - "Best practices section highlights important considerations for scalable, maintainable multi-agent systems."
    - "Related concepts section helps readers explore foundational building blocks and abstractions."
  recommendations:
    - "Update code examples to be fully runnable and eliminate placeholders or undefined variables."
    - "Add a troubleshooting/limitations section to help users avoid or diagnose common issues with swarms and nested agents."
    - "Consider including a visual diagram or flowchart to illustrate agent orchestration and transitions."
    - "Break up dense text with bullet points, subheadings, or diagrams to improve readability and approachability for a broader audience."
```


## Content

```yaml
content:
  overview: |
    Swarm and Nested Agents are advanced patterns for orchestrating multiple agents in dynamic, collaborative, or hierarchical workflows. These patterns enable the creation of agent "swarms" (large, parallel groups of agents), nesting (agents managing sub-chats or delegating tasks to sub-agents), and sophisticated transition logic between agents or agent groups. They facilitate scalable, modular, and context-aware multi-agent systems suitable for complex automation, problem-solving, or simulation scenarios.

  explanation: |
    In agent frameworks, a "swarm" refers to a group of agents collaborating—often in parallel or with dynamic coordination—to solve a problem or process tasks. The swarm pattern leverages abstractions like `GroupChat` and `GroupChatManager` to manage agent membership, conversation state, and orchestration logic (e.g., round-robin, auto-selection, or custom strategies).

    Nested agents extend this idea by allowing agents to initiate, manage, or participate in sub-chats or sub-groups (i.e., "nested" group chats), enabling hierarchical workflows. For example, a manager agent could delegate sub-tasks to specialized agents, each of whom may further orchestrate their own group of sub-agents.

    Advanced transitions allow for flexible handoffs and control flows between agents or groups, using constructs like `TransitionTarget`, `OnCondition`, and `OnContextCondition`. These enable dynamic routing of conversation or task ownership based on LLM outputs, context, or custom rules.

    The core agent abstraction (`ConversableAgent` and its protocol) supports these patterns by providing message handling, tool integration, and chat management. Group orchestration is abstracted via `GroupChat`, `GroupChatManager`, and patterns such as `AutoPattern`, which encapsulate different strategies for agent selection and transition.

  examples:
    - title: "Creating a Swarm of Agents for Parallel Task Solving"
      description: |
        This example demonstrates orchestrating a swarm of agents to collaboratively solve sub-tasks using an auto pattern for speaker selection.
      code: |
        from autogen import ConversableAgent, GroupChat, GroupChatManager
        from autogen.agentchat.group.patterns.auto import AutoPattern

        # Create individual agents
        agents = [
            ConversableAgent(name=f"worker_{i}", system_message="You are a domain expert.", llm_config={...})
            for i in range(5)
        ]

        # Define a swarm orchestration pattern
        pattern = AutoPattern(initial_agent=agents[0], agents=agents)

        # Prepare the group chat (the swarm)
        groupchat, manager = pattern.prepare_group_chat(max_rounds=10, messages=[{"content": "Solve the problem"}])

        # Initiate the swarm conversation
        agents[0].initiate_chat(manager, message="Let's break down the task.")

    - title: "Nested Group Chat: Manager Agent Delegates to Expert Subgroups"
      description: |
        This example shows a manager agent that can spawn and manage a nested group chat to solve a sub-task, demonstrating hierarchical agent orchestration.
      code: |
        from autogen import ConversableAgent, GroupChatManager
        from autogen.agentchat.group.patterns.auto import AutoPattern

        # Define expert agents
        experts = [ConversableAgent(name=f"expert_{i}", llm_config={...}) for i in range(3)]
        expert_pattern = AutoPattern(initial_agent=experts[0], agents=experts)
        expert_groupchat, expert_manager = expert_pattern.prepare_group_chat(max_rounds=5)

        # Define the manager agent
        class ManagerAgent(ConversableAgent):
            def generate_reply(self, messages, sender, config):
                # On a specific trigger, start a nested group chat
                if "delegate to experts" in messages[-1]["content"]:
                    # Start conversation with the expert manager (nested chat)
                    self.initiate_chat(expert_manager, message="Please handle this sub-task.")
                    return "Delegated sub-task to expert group."
                return super().generate_reply(messages, sender, config)

        manager = ManagerAgent(name="manager", llm_config={...})
        manager.initiate_chat(expert_manager, message="delegate to experts")

    - title: "Conditional Agent Handoff with OnCondition"
      description: |
        Use condition-based transitions to dynamically select the next agent based on message content.
      code: |
        from autogen.agentchat.group.transition import OnCondition, TransitionTarget
        from autogen.agentchat.group.patterns.auto import AutoPattern

        def is_financial_question(content):
            return "finance" in content

        pattern = AutoPattern(
            agents=[agent_a, agent_b],
            transitions=[
                OnCondition(
                    condition=lambda m: is_financial_question(m["content"]),
                    target=TransitionTarget(agent="finance_expert")
                )
            ]
        )
        groupchat, manager = pattern.prepare_group_chat()

  best_practices:
    - "Assign unique, descriptive names to all agents in a swarm or nested group to aid tracking and debugging."
    - "Use orchestration patterns (e.g., AutoPattern, RoundRobin) to encapsulate agent selection logic; avoid hardcoding transitions."
    - "Manage and prune chat history in large swarms or nested chats to prevent memory bloat."
    - "Explicitly handle nested chat lifecycles (start, monitor, and end sub-chats) to prevent orphaned or dangling conversations."
    - "Use condition-based transitions (OnCondition, OnContextCondition) for adaptive, context-aware handoff logic."
    - "Thoroughly test complex group and nested workflows—log messages and transitions for observability."
    - "Document agent roles and transition logic for maintainability, especially when nesting or chaining swarms."

  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "Provide the core interface and logic for all agents, enabling message handling and multi-agent workflows."
    - name: "GroupChat and GroupChatManager"
      description: "Support orchestration, message routing, and group state management for swarms and nested agent groups."
    - name: "Patterns (AutoPattern, RoundRobin, etc.)"
      description: "Encapsulate reusable strategies for orchestrating agent interactions in swarms or hierarchies."
    - name: "TransitionTarget and OnCondition"
      description: "Enable flexible, context-sensitive transitions and handoffs between agents or groups."
    - name: "Tool and Toolkit"
      description: "Allow agents (including swarms and nested agents) to access and share toolsets for function-calling and problem-solving."
    - name: "LLMConfig"
      description: "Standardizes LLM setup across all agents, ensuring consistent model use in swarms and nested chats."
```