# Quick Start


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The code examples assume that 'autogen' and its submodules are installed and available, but installation/setup is not mentioned anywhere in the Quick Start."
      severity: "medium"
      suggestion: "Add a note or a code snippet about installation requirements (e.g., pip install autogen) at the start of the section."
    - type: "Clarity"
      description: "Some terms (e.g., 'LLM', 'function-calling', 'orchestration pattern') are used before being fully defined, which may be unclear for absolute beginners."
      severity: "low"
      suggestion: "Briefly define such terms or provide a link/reference to a glossary or introductory section."
    - type: "Completeness"
      description: "The section covers many core abstractions, but lacks a brief summary or flow diagram that visually connects these concepts for new users."
      severity: "low"
      suggestion: "Add a conceptual diagram or a workflow summary after the overview."
    - type: "Code Example Quality"
      description: "Some code examples (such as 'agent.initiate_chat(user, message=...)') omit expected output or results, which can leave users uncertain of what to expect."
      severity: "medium"
      suggestion: "Add a comment or print statement showing the expected output/result for each example."
    - type: "Best Practices Coverage"
      description: "The best practices focus on technical details, but don't mention error handling, debugging, or safe API usage."
      severity: "low"
      suggestion: "Add best practices on handling exceptions, logging, or rate limiting when using LLM APIs."

  strengths:
    - "Thorough, structured coverage of the most important abstractions and use cases in the framework."
    - "Code examples directly map to the concepts described, and are concise, relevant, and easy to follow."
    - "Best practices section provides practical, actionable advice for setting up and managing agents and tools."
    - "Related concepts give users a clear sense of what to explore next."

  recommendations:
    - "Include installation/setup instructions at the start of the Quick Start to prevent user confusion."
    - "Augment code examples with expected outputs or usage notes to clarify what users should see after running the samples."
    - "Consider adding a visual component (diagram or flowchart) to help users understand how agents, tools, and group chats interconnect."
    - "Expand best practices to include guidance on error handling and safe management of API credentials."
```


## Content

```yaml
content:
  overview: |
    The Quick Start section provides basic usage examples to help you rapidly get up and running with the core abstractions of the agent framework. You will learn how to instantiate conversational agents, register tools (functions) for LLM use, set up multi-agent group chats, and configure LLM providers. These foundational patterns form the basis for building more complex agentic workflows and multi-agent systems.

  explanation: |
    This section introduces you to the essential building blocks for agentic communication and orchestration:
      - **ConversableAgent**: The primary agent abstraction, supporting messaging, tool integration, and both single- and multi-agent interactions.
      - **Tools and Toolkits**: Mechanisms for exposing callable Python functions to LLM agents, enabling dynamic function calling and workflow extension.
      - **GroupChat and Patterns**: Facilities for structuring conversations among multiple agents, including orchestration strategies and transition management.
      - **LLMConfig**: Unified configuration and management for LLM providers, supporting environment-based setup and advanced filtering.
    
    Through hands-on examples, you'll see how to:
      - Instantiate and configure agents
      - Register tools for LLM and execution
      - Initiate chats between agents or with groups
      - Manage LLM provider configuration

    These patterns are extensible and composable, enabling you to build everything from simple chatbots to sophisticated, tool-using, multi-agent systems.

  examples:
    - title: "Creating and Chatting with a ConversableAgent"
      description: "Set up a basic agent, register a tool, and initiate a chat."
      code: |
        from autogen import ConversableAgent

        # Create a basic agent with a system message and LLM configuration
        agent = ConversableAgent(
            name="assistant",
            system_message="You are a helpful AI assistant.",
            llm_config={"model": "gpt-3.5-turbo", "api_key": "..."}
        )

        # Register a function as a tool for the agent
        @agent.register_for_llm()
        def add(a: int, b: int) -> int:
            return a + b

        # Create another agent to chat with
        user = ConversableAgent(name="user", system_message="You are a user.")

        # Start a conversation
        result = agent.initiate_chat(user, message="Hello! Can you add 3 and 5?")
    - title: "Defining and Registering Tools via Toolkits"
      description: "Create tools with decorators, group them in a toolkit, and register with an agent."
      code: |
        from autogen.tools import tool, Toolkit

        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a: int, b: int) -> int:
            return a * b

        toolkit = Toolkit([multiply])
        # Register all tools in the toolkit for LLM function-calling
        toolkit.register_for_llm(agent)
    - title: "Orchestrating a Group Chat with Multiple Agents"
      description: "Set up a group chat with two agents and an automatic orchestration pattern."
      code: |
        from autogen import GroupChat, GroupChatManager, ConversableAgent
        from autogen.agentchat.group.patterns.auto import AutoPattern

        agent1 = ConversableAgent("agent1")
        agent2 = ConversableAgent("agent2")

        agents = [agent1, agent2]
        pattern = AutoPattern(initial_agent=agent1, agents=agents)
        groupchat, manager = pattern.prepare_group_chat(max_rounds=5, messages=[{"content": "Hello group!"}])

        # Start the group chat
        agent1.initiate_chat(manager, message="Let's collaborate!")
    - title: "Configuring LLM Providers with LLMConfig"
      description: "Set up agent LLM configuration from environment settings."
      code: |
        from autogen.llm_config import LLMConfig

        # Load configuration from a JSON environment variable (e.g., OAI_CONFIG_LIST)
        config = LLMConfig.from_json(env="OAI_CONFIG_LIST")
        agent = ConversableAgent("my_agent", llm_config=config)
    - title: "Registering a Tool for Execution Only"
      description: "Allow the agent to execute a tool without exposing it for LLM function-calling."
      code: |
        @agent.register_for_execution()
        def subtract(a: int, b: int) -> int:
            return a - b

  best_practices:
    - "Always provide unique, descriptive names for agents and tools to avoid ambiguity in multi-agent or tool-rich settings."
    - "Register all tools before starting any conversation to ensure they are available to LLMs."
    - "Use decorators (e.g., @tool or @agent.register_for_llm()) for tool registration to promote clarity and maintainability."
    - "Explicitly set 'human_input_mode' when creating agents to control if/when user prompts are allowed."
    - "Group related tools using Toolkits for easier management and registration."
    - "Manage chat history size in group chats to prevent excessive memory usage."
    - "Use environment variables or secure storage for API keys and LLM provider credentials."

  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "Foundation for all agent types; enables messaging, tool use, and agent-to-agent interaction."
    - name: "Tool and Toolkit"
      description: "Mechanism for exposing Python functions to agents and LLMs for dynamic function-calling."
    - name: "GroupChat and Patterns"
      description: "Orchestrates multi-agent conversations, speaker selection, and workflow management."
    - name: "LLMConfig"
      description: "Centralized management of LLM provider configurations for agents and clients."
    - name: "Tool Interoperability"
      description: "Supports converting tools from other ecosystems (e.g., LangChain, CrewAI) for use within this framework."
```