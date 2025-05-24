content:
  overview: |
    Group Chat Patterns provide structured approaches for orchestrating multi-agent conversations, enabling agents to interact, collaborate, and coordinate tasks in group settings. These patterns abstract away the complexities of speaker selection, message routing, handoffs, and conversational flow management, making it easier to build robust multi-agent workflows.

  explanation: |
    In multi-agent systems, orchestrating group conversations is non-trivial. Effective group chat requires managing which agent speaks next, how information is passed, and when control transitions between agents. Group Chat Patterns encapsulate these orchestration strategies, allowing developers to focus on high-level workflows rather than low-level agent control.

    The core abstractions include:

    - **ConversableAgent and Agent Protocols**: These form the backbone for all agent communication. Agents can send and receive messages, register tools, and maintain chat history. In group settings, each agent participates as a member of the group chat.
    - **GroupChat**: Represents the state and membership of the group conversation, including a list of agents, the message history, and parameters such as the maximum number of rounds.
    - **GroupChatManager**: Acts as the conductor, managing the flow of the conversation, speaker selection, and the application of orchestration patterns.
    - **Patterns**: Reusable strategies that dictate how agents take turns, how transitions are handled, and how handoffs occur. Examples include round-robin, LLM-based selection (AutoPattern), manual, and random.
    - **Transitions and Handoffs**: Mechanisms for context-sensitive agent switching, allowing for dynamic, condition-based control transfer.

    By leveraging these abstractions and patterns, developers can implement complex collaborative behaviors (e.g., brainstorming, debate, workflow handoffs) with minimal boilerplate and maximum flexibility. The provided patterns are extensible, and custom strategies can be implemented for specialized needs.

  examples:
    - title: "Setting up a basic group chat with automatic speaker selection"
      description: "Create two agents and orchestrate a conversation using the AutoPattern, which leverages LLM-based logic for speaker selection."
      code: |
        from autogen import ConversableAgent
        from autogen.agentchat.group.patterns.auto import AutoPattern

        # Create agents
        assistant = ConversableAgent(
            name="assistant",
            system_message="You are a helpful assistant."
        )
        expert = ConversableAgent(
            name="expert",
            system_message="You are a domain expert."
        )

        # Set up the group chat pattern
        agents = [assistant, expert]
        pattern = AutoPattern(initial_agent=assistant, agents=agents)

        # Prepare the group chat and manager
        groupchat, manager = pattern.prepare_group_chat(
            max_rounds=5,
            messages=[{"content": "Let's solve the problem together."}]
        )

        # Start the conversation
        assistant.initiate_chat(manager, message="What are your thoughts?")
    - title: "Custom speaker selection logic"
      description: "Define a custom function for selecting the next speaker in the group."
      code: |
        def round_robin_selector(last_speaker, groupchat):
            # Simple round-robin: pick the next agent in the list
            idx = groupchat.agents.index(last_speaker)
            return groupchat.agents[(idx + 1) % len(groupchat.agents)]

        from autogen.agentchat.group.patterns.auto import AutoPattern

        pattern = AutoPattern(
            initial_agent=assistant,
            agents=agents,
            group_manager_args={"speaker_selection_method": round_robin_selector}
        )
        groupchat, manager = pattern.prepare_group_chat(max_rounds=3)
    - title: "Condition-based handoff using OnCondition"
      description: "Use OnCondition to trigger agent transitions based on message content."
      code: |
        from autogen.agentchat.group.transition import OnCondition, TransitionTarget

        # Define a transition: If a message contains 'expert', switch to expert agent
        on_expert_condition = OnCondition(
            condition=lambda msg, ctx: 'expert' in msg['content'].lower(),
            target=TransitionTarget(agent=expert)
        )

        # Pass this transition to the group pattern or manager as needed

  best_practices:
    - "Use predefined patterns (Auto, RoundRobin, etc.) to encapsulate orchestration logic and avoid manual agent selection."
    - "Assign unique, descriptive names to all agents to simplify debugging and log tracing."
    - "Carefully manage chat history in group settings to prevent memory bloat and ensure relevant context."
    - "Validate agent and transition configurations to avoid runtime errors (e.g., duplicate names, unreachable agents)."
    - "Leverage condition-based transitions (OnCondition, OnContextCondition) for flexible, context-aware workflows."
    - "Test group chat flows with logging enabled to diagnose complex handoff and orchestration issues."

  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "Define the standard communication interface for agents, used as the basis for group chat participants."
    - name: "Tool and Toolkit"
      description: "Agents in group chats often collaborate by invoking tools; registering tools before chat initiation ensures visibility and interoperability."
    - name: "LLMConfig and LLMConfigEntry"
      description: "Standardize LLM configuration across agents in a group, preventing provider mismatch and supporting context management."
    - name: "Transitions and Handoffs"
      description: "Allow dynamic, rule-based switching of control between agents, critical for sophisticated workflow modeling in group chats."
    - name: "Tool Interoperability"
      description: "Enables agents to share and use tools from different ecosystems, expanding collaborative capabilities in group settings."