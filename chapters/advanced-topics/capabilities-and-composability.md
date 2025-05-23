```yaml
content:
  overview: |
    Capabilities and composability are foundational principles in modern agent frameworks. They empower agents to be extended with new skills (capabilities) such as memory, vision, tool usage, and transformation pipelines, and to compose these modularly for complex behaviors. This approach enables flexible, reusable, and scalable agent designs, where agents can dynamically acquire, combine, and orchestrate diverse abilities in various task and group settings.

  explanation: |
    In advanced agent frameworks, "capabilities" refer to pluggable functionalities that enhance an agent's intelligence and interaction. These include memory (tracking context/history), perception (e.g., vision modules for images), tool usage (external functions/APIs), and transforms (pre/post-processing of data or messages). "Composability" describes the agent's ability to combine these capabilities—either by direct registration, delegation to group managers, or protocol-driven integration—allowing for highly adaptive and task-specific behaviors.

    The framework achieves this via well-defined abstractions:
      - **ConversableAgent and Agent Protocols**: Establish the standard interface for agent communication and behavior, providing hooks for registering capabilities and tools.
      - **Tool and Toolkit**: Formalize callable functions/APIs as tools, which agents can use or propose in conversation, with robust type and metadata support.
      - **GroupChat and Orchestration Patterns**: Enable multi-agent interactions, role transitions, and group workflows, where composability allows agents with different or overlapping capabilities to collaborate.
      - **LLMConfig**: Standardizes how language model backends and context are managed and composed, crucial for agents that may dynamically switch models or providers.
      - **Tool Interoperability**: Facilitates the conversion and integration of tools from external ecosystems (e.g., LangChain, CrewAI) into the agent's toolset, further amplifying composability.

    These abstractions allow for agents that can, for example, remember previous interactions, analyze images, call external APIs, collaborate in groups, and adapt their workflow based on changing requirements—all via modular, composable configuration.

  examples:
    - title: "Composing an Agent with Memory and Tool Use"
      description: "Demonstrates creating an agent with chat memory and arithmetic tool capabilities."
      code: |
        from autogen import ConversableAgent
        from autogen.tools import tool

        # Define a simple arithmetic tool
        @tool(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        # Create an agent and register the tool
        agent = ConversableAgent(
            name="math_assistant",
            system_message="You are a helpful math assistant.",
            llm_config={...},
            memory=True  # Enable memory capability
        )
        agent.register_tool(add)

        # Start a conversation using the composed capabilities
        result = agent.initiate_chat(
            other_agent,
            message="What is the sum of 7 and 8?"
        )

    - title: "Extending an Agent with Vision Capability"
      description: "Shows how to add image analysis to an agent using a vision tool."
      code: |
        from autogen import ConversableAgent
        from autogen.tools.vision import analyze_image

        vision_agent = ConversableAgent(
            name="vision_bot",
            system_message="You can describe images.",
            llm_config={...}
        )

        # Register vision tool
        vision_agent.register_tool(analyze_image)

        # Use the agent to analyze an image
        result = vision_agent.initiate_chat(
            user_proxy,
            message="Please describe the attached image.",
            attachments=["/path/to/image.png"]
        )

    - title: "Multi-Agent Group with Diverse Capabilities"
      description: "Orchestrates a group chat where agents have different capabilities (e.g., one with tools, one with memory)."
      code: |
        from autogen import GroupChat, GroupChatManager, ConversableAgent
        from autogen.tools import tool

        @tool(name="lookup", description="Lookup a fact")
        def lookup_fact(query: str) -> str:
            # ... implementation ...
            return "42"

        agent_a = ConversableAgent("fact_agent", memory=False)
        agent_b = ConversableAgent("history_agent", memory=True)
        agent_a.register_tool(lookup_fact)

        group_chat = GroupChat([agent_a, agent_b])
        manager = GroupChatManager(group_chat)
        agent_a.initiate_chat(manager, message="Let's solve a problem.")

    - title: "Interoperability: Importing a LangChain Tool"
      description: "Illustrates converting a LangChain tool into a framework-compatible tool for use in an agent."
      code: |
        from autogen.tools.interop.langchain import from_langchain_tool
        from langchain.tools import SomeLangChainToolClass

        lc_tool = SomeLangChainToolClass(...)
        ag2_tool = from_langchain_tool(lc_tool)

        agent = ConversableAgent(name="interop_agent", llm_config={...})
        agent.register_tool(ag2_tool)

  best_practices:
    - "Design agent capabilities as focused, modular components to maximize reusability."
    - "Always register tools and capabilities before initiating chats to ensure LLMs and agents can utilize them."
    - "Use descriptive names and type hints for tools and capabilities to help LLMs reason and compose actions."
    - "Manage agent memory scope (e.g., conversation length) to avoid performance or privacy issues."
    - "Leverage toolkits and interoperability registries to organize and scale up agent skills."
    - "Test agent compositions in both isolated and group settings to catch orchestration issues early."
    - "Use transform hooks for custom pre/post-processing logic without modifying core agent code."

  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "Provide the extensible foundation for all agent capabilities and composability; agents register tools, memory, and transforms via this abstraction."
    - name: "Tool and Toolkit"
      description: "Formalize callable functions as capabilities, supporting both LLM-driven and direct execution; essential for composable agent skill sets."
    - name: "GroupChat and Orchestration Patterns"
      description: "Enable multi-agent workflows, leveraging composable agents with diverse capabilities and orchestrating them via patterns."
    - name: "LLMConfig"
      description: "Standardizes language model configuration, supporting context-aware composition of LLM capabilities."
    - name: "Tool Interoperability"
      description: "Expands composability by allowing tools from other ecosystems to be integrated as agent capabilities."
    - name: "Memory and Transform Hooks"
      description: "Memory tracks context/history as a capability; transform hooks provide customizable pre/post-processing, furthering composability."
```
