# Agents and Conversations


## Quality Check

quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The code examples assume a certain API without specifying the framework/library version (e.g., 'autogen'). The usage of methods like `register_for_llm()` and `initiate_chat()` may not be standard or could have changed depending on the latest framework version."
      severity: "medium"
      suggestion: "Clarify the framework version or provide a note about API version compatibility. Ensure that all example code is up to date with the latest stable release."
    - type: "Clarity"
      description: "The explanation is dense and uses jargon (e.g., 'orchestration patterns', 'protocol', 'toolkits') without always defining them or linking to definitions."
      severity: "medium"
      suggestion: "Add brief definitions or links to related concept sections for key terms when they first appear."
    - type: "Completeness"
      description: "The documentation describes core agent types and group chat patterns, but does not mention error handling, security considerations, or limitations of the framework."
      severity: "low"
      suggestion: "Add a brief subsection or notes about common errors, limitations, or security best practices when using agents and conversations."
    - type: "Code Example Quality"
      description: "The code examples are concise and relevant but lack import context for some functions (e.g., `register_for_llm()` is used without clear prior definition in the framework; also, `llm_config={...}` is a placeholder that may confuse readers)."
      severity: "medium"
      suggestion: "Add comments or explanatory notes for placeholders (such as `llm_config={...}`), and clarify the origin or definition of less-common methods."
    - type: "Best Practices Coverage"
      description: "Best practices cover operational and design topics, but do not reference security, privacy, or troubleshooting."
      severity: "low"
      suggestion: "Expand best practices to include a point on securing conversations (e.g., sanitizing tool inputs/outputs) and handling common errors."
  strengths:
    - "Comprehensive overview of agents, conversations, and group chat patterns, providing both high-level abstraction and practical usage."
    - "Well-structured code examples that illustrate typical agent usage, tool registration, and group chat orchestration."
  recommendations:
    - "Clarify framework/library version compatibility in the documentation and ensure all code examples are up to date with the latest API."
    - "Expand on definitions for technical terms and add contextual notes or links for deeper exploration."
    - "Enhance best practices with a focus on security, error handling, and limitations."
    - "Supplement code examples with comments or explanations for any placeholders or advanced methods to aid new users."


## Content

content:
  overview: |
    Agents and Conversations are fundamental to building intelligent, interactive systems using the framework. Agents represent autonomous entities capable of sending and receiving messages, executing tools, and collaborating in both simple one-on-one and complex multi-agent group chats. Conversations refer to the structured interactions between these agents, often managed and orchestrated through group chat patterns and managers.
  explanation: |
    An **Agent** is an abstraction for any entity (human, AI, or system) that can participate in a conversation. The core agent type, `ConversableAgent`, provides built-in capabilities for managing chat history, sending/receiving messages, auto-replying, and registering tools (callable functions that the agent can invoke via LLMs). Specialized agent types (like `AssistantAgent`, `UserProxyAgent`, and `GroupChatManager`) extend this core logic to support various roles and workflows.

    Conversations are initiated when agents exchange messages. In the simplest case, two agents (e.g., a user and an assistant) interact directly. For more complex scenarios, the **GroupChat** abstraction allows multiple agents to participate in structured group conversations, orchestrated by a `GroupChatManager` according to flexible "patterns" (such as round-robin, LLM-based, or manual speaker selection). Tools and toolkits can be registered with agents, enabling them to perform actions or computations during a conversation.

    The framework abstracts away the complexity of agent orchestration, message routing, and group transitions, allowing developers to focus on high-level conversational logic and collaborative workflows. At its core, every agent implements a protocol (interface) for communication, ensuring composability and extensibility.

  examples:
    - title: "Setting Up a Simple Agent Conversation"
      description: "Create two agents and initiate a chat between them."
      code: |
        from autogen import ConversableAgent

        assistant = ConversableAgent(
            name="assistant",
            system_message="You are a helpful AI.",
            llm_config={...}
        )
        user = ConversableAgent(name="user")

        assistant.initiate_chat(user, message="Hello! How can I help you?")
    - title: "Registering a Tool for Function Calling"
      description: "Attach a function as a callable tool to an agent so the LLM can use it during conversation."
      code: |
        from autogen.tools import tool

        @tool(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        assistant.register_for_llm()(add)
    - title: "Creating a Group Chat with Orchestration Pattern"
      description: "Set up a group chat with two agents and an auto pattern for speaker selection."
      code: |
        from autogen import GroupChat, GroupChatManager, ConversableAgent
        from autogen.agentchat.group.patterns.auto import AutoPattern

        agents = [ConversableAgent("a1"), ConversableAgent("a2")]
        pattern = AutoPattern(initial_agent=agents[0], agents=agents)
        groupchat, manager = pattern.prepare_group_chat(max_rounds=10, messages=[{"content": "Start"}])

        agents[0].initiate_chat(manager, message="Let's begin")
    - title: "Customizing Speaker Selection in Group Chat"
      description: "Define a custom function for choosing the next speaker in a group chat."
      code: |
        def my_selector(last_speaker, groupchat):
            # Custom logic to pick next agent; for example, alternate speakers
            return groupchat.next_agent(last_speaker)

        pattern = AutoPattern(
            initial_agent=agents[0],
            agents=agents,
            group_manager_args={"speaker_selection_method": my_selector}
        )
  best_practices:
    - "Always give each agent a unique, descriptive name to avoid confusion in logs and message routing."
    - "Explicitly set `human_input_mode` for agents to control when user input is required and prevent unexpected prompts."
    - "Register tools and toolkits with agents before starting a conversation to ensure availability for LLM function calls."
    - "Leverage orchestration patterns (e.g., AutoPattern, RoundRobinPattern) for group chats instead of manual agent selection logic."
    - "Manage chat history carefully in group settings to avoid excessive memory usage; consider truncating or summarizing history as needed."
    - "When extending agent classes or overriding methods, use `super()` to preserve base functionality."
    - "Validate group chat configurations (agent names, transitions, speaker patterns) early to prevent runtime errors."
    - "Test group chat workflows and log interactions to facilitate debugging complex agent behaviors."
  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "The foundational abstraction for all agent communication, supporting messaging, tool registration, and extensibility."
    - name: "Tool and Toolkit"
      description: "Encapsulate callable functions for agents, enabling LLM-driven function execution during conversations."
    - name: "GroupChat and GroupChatManager"
      description: "Facilitate orchestrated, multi-agent conversations with configurable speaker selection and workflow patterns."
    - name: "Patterns (AutoPattern, RoundRobinPattern, etc.)"
      description: "Reusable strategies for managing the flow of group conversations—who speaks next, transitions, and handoffs."
    - name: "LLMConfig"
      description: "Defines and manages configuration for language model providers, ensuring agents use the correct models and credentials."
    - name: "Tool Interoperability"
      description: "Allows integration of tools from other ecosystems, enabling agents to use a wide variety of external functions in conversation."