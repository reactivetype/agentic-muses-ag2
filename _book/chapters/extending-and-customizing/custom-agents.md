content:
  overview: |
    Custom Agents allow you to extend the core agent framework by defining your own agent classes with specialized behaviors, capabilities, and integrations. By subclassing the foundational ConversableAgent or implementing the Agent protocol, you can create agents that interact, reason, manage tools, and participate in group settings according to your unique requirements. Registering your custom agents ensures they are discoverable and usable within the broader agent ecosystem.
  explanation: |
    The framework is built around the `ConversableAgent` abstraction, which encapsulates agentic communication, tool usage, and messaging workflows. To tailor agents for advanced scenarios—such as domain-specific reasoning, custom tool integration, or unique conversational logic—you can define your own agent classes.

    Custom agents are typically created by either:
      - **Subclassing ConversableAgent**: Inherit its robust messaging, tool management, and reply logic, and override or extend methods to customize behavior.
      - **Implementing the Agent Protocol**: Define the required interface (`name`, `description`, `send`, `receive`, `generate_reply`, etc.) if you need lower-level or non-standard agent logic.

    After creating a custom agent class, you can instantiate agents, register tools (functions or toolkits), and participate in direct or group conversations. Registering agents with orchestration components (e.g., GroupChatManager, registries) makes them accessible for workflows like multi-agent chat or automated handoffs.

    **Key extension points include:**
      - Overriding `generate_reply` for custom message handling.
      - Registering tools with `register_for_llm` or `register_tool` for LLM function-calling.
      - Customizing chat history, system messages, or reply triggers.
      - Integrating with external systems or APIs.

    This flexibility enables you to build agents for tasks such as domain-specific assistants, workflow organizers, API bridges, or even simulation bots.

  examples:
    - title: "Subclassing ConversableAgent for Domain-Specific Logic"
      description: |
        Create a custom agent that gives weather advice by overriding the reply generation method.
      code: |
        from autogen import ConversableAgent

        class WeatherAgent(ConversableAgent):
            def generate_reply(self, messages, sender, config, **kwargs):
                last_message = messages[-1]['content']
                if "weather" in last_message.lower():
                    return "The weather is sunny today. 🌞"
                return super().generate_reply(messages, sender, config, **kwargs)

        agent = WeatherAgent(
            name="weather_bot",
            system_message="You are a weather assistant.",
            llm_config={...}
        )
        user = ConversableAgent(name="user", human_input_mode="ALWAYS")
        agent.initiate_chat(user, message="What's the weather?")
    - title: "Implementing the Agent Protocol Directly"
      description: |
        Build a lightweight agent by implementing only the protocol, suitable for non-chat or API-based logic.
      code: |
        from autogen.agentchat.agent import Agent

        class EchoAgent(Agent):
            def __init__(self, name):
                self.name = name
                self.description = "Echoes all messages."
            def send(self, message, recipient, **kwargs):
                recipient.receive(f"Echo: {message}", sender=self)
            def receive(self, message, sender, **kwargs):
                self.send(message, sender)
            def generate_reply(self, messages, sender, config, **kwargs):
                return f"Echo: {messages[-1]['content']}"

        echo = EchoAgent("echoer")
        # Use with a ConversableAgent or in a group chat
    - title: "Registering and Using Tools in a Custom Agent"
      description: |
        Equip your custom agent with tools, allowing LLMs to call functions via tool registration.
      code: |
        from autogen import ConversableAgent
        from autogen.tools import tool

        class MathAgent(ConversableAgent):
            pass

        math_agent = MathAgent(name="math_bot", system_message="You solve math problems.", llm_config={...})

        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a: int, b: int) -> int:
            return a * b

        math_agent.register_for_llm()(multiply)
        # Now, LLMs can invoke 'multiply' during chat!

  best_practices:
    - "Always give each custom agent a unique, descriptive name to avoid confusion in group or multi-agent settings."
    - "Prefer subclassing ConversableAgent for most use cases to leverage built-in chat and tool logic."
    - "Register all tools and reply hooks before starting chats; late registration can result in missing capabilities."
    - "When overriding methods like generate_reply, call super() if you want to retain default behaviors."
    - "Explicitly set human_input_mode for agents to prevent unexpected prompts in automated flows."
    - "Carefully manage chat history, especially in group contexts, to avoid excessive memory usage."
    - "Test custom agents in isolation before integrating them into orchestrated group patterns."
    - "Document custom behaviors and expected inputs/outputs for maintainability."

  related_concepts:
    - name: "ConversableAgent (and Agent Protocols)"
      description: "The foundational abstraction for agent behavior and communication; custom agents typically extend this."
    - name: "Tool and Toolkit"
      description: "Encapsulate functions your custom agent can call; register these with your agent for LLM use."
    - name: "GroupChat, GroupChatManager, and Patterns"
      description: "Allow custom agents to participate in structured multi-agent workflows and orchestrations."
    - name: "LLMConfig and LLMConfigEntry"
      description: "Define model configuration for your custom agent, enabling use of various LLM providers."
    - name: "Tool Interoperability"
      description: "Facilitates integration of tools from other ecosystems; useful if your custom agent needs external toolkits."
    - name: "Hooks and Reply Functions"
      description: "Custom agents can register hooks or reply functions to further customize message handling."
    - name: "Orchestration Patterns"
      description: "Patterns like AutoPattern, RoundRobin, etc., enable your custom agents to operate in coordinated group scenarios."