content:
  overview: |
    Tools and toolkits are foundational abstractions in agentic frameworks that enable agents to perform actions beyond conversation. By registering tools (callable functions or APIs) with agents, you empower them to execute code, call external services, or use structured function-calling capabilities in LLMs. Toolkits group related tools for modular and scalable management. Dependency injection ensures that tools receive the correct context or resources when executed, supporting clean separation of concerns and extensibility.

  explanation: |
    In an agent framework, a "tool" is a callable object (typically a function) that an agent can invoke—either directly or via language model (LLM) function-calling—to perform a task. Tools can range from simple mathematical operations to complex API calls or workflow triggers.

    Agents, such as those derived from `ConversableAgent`, use tools to extend their capabilities beyond pure language processing. Tools must be registered with an agent for the agent (and the underlying LLM) to recognize and propose their use. This is typically done via decorators (e.g., `@tool`), direct registration (e.g., `register_tool`), or via a `Toolkit`—a container for managing multiple tools as a unit.

    Tool registration associates metadata (name, description, parameter schema) with a callable, making it discoverable and usable by both the agent and function-calling LLMs. Registration also supports execution routing, so an agent can both propose and directly execute tools as needed.

    Dependency injection allows for advanced tool scenarios, where tools can automatically receive required context (e.g., the calling agent, the message context, or other dependencies) without manual wiring. This enables tools to remain decoupled and reusable.

    Toolkits are collections of related tools, providing batch registration and collective management. They foster modularity, allowing you to assemble and share sets of capabilities across agents or projects.

    Properly describing and registering tools, and using dependency injection judiciously, ensures that agents can reliably reason about and use available capabilities. This unlocks powerful patterns for agentic reasoning, automation, and interoperability with external tool ecosystems.

  examples:
    - title: "Defining and Registering a Tool with an Agent"
      description: "Use the `@tool` decorator to create a tool and register it for LLM function-calling."
      code: |
        from autogen.tools import tool
        from autogen import ConversableAgent

        @tool(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        agent = ConversableAgent("math_agent")
        agent.register_for_llm()(add)  # Register for LLM function-calling

    - title: "Using a Toolkit to Group and Register Tools"
      description: "Bundle multiple tools into a toolkit and register them with an agent."
      code: |
        from autogen.tools import tool, Toolkit
        from autogen import ConversableAgent

        @tool(name="subtract", description="Subtract two numbers")
        def subtract(a: int, b: int) -> int:
            return a - b

        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a: int, b: int) -> int:
            return a * b

        toolkit = Toolkit([subtract, multiply])

        agent = ConversableAgent("calculator")
        toolkit.register_for_llm(agent)  # Register all tools for LLM use

    - title: "Registering a Tool for Execution or Dual Use"
      description: "Control whether a tool is available for LLM proposal, execution, or both."
      code: |
        agent.register_for_execution()(add)     # Only for execution (not LLM proposal)
        agent.register_tool(add)                # Both propose (LLM) and execute

    - title: "Dependency Injection in Tool Functions"
      description: "Inject agent or context into tools, enabling advanced behaviors."
      code: |
        from autogen.tools import tool

        @tool
        def greet(name: str, agent=None):
            return f"Hello, {name}! I am {agent.name if agent else 'an agent'}."

        agent = ConversableAgent("greeter")
        agent.register_tool(greet)
        # When called via the agent, `agent` will be injected automatically.

  best_practices:
    - "Always provide clear, concise names and descriptions for each tool."
    - "Use Python type hints for all tool parameters to ensure proper schema generation."
    - "Prefer the `@tool` decorator for defining tools to promote clarity and reduce boilerplate."
    - "Register all necessary tools before starting a chat or agent session."
    - "Leverage toolkits to organize related tools and manage them as a group."
    - "Use dependency injection only when necessary and document injectable parameters clearly."
    - "Avoid mutating agent state within tools unless intended and well-documented."
    - "Test tool registration and execution paths to catch schema or signature mismatches early."

  related_concepts:
    - name: "ConversableAgent (and Agent Protocols)"
      description: |
        Agents use tools to extend their abilities. The ConversableAgent abstraction provides the mechanisms for tool registration, management, and invocation within agentic workflows.
    - name: "LLM Function Calling"
      description: |
        Registered tools are exposed to LLMs for structured function calling, allowing models to propose tool usage during conversations.
    - name: "Toolkit"
      description: |
        Toolkits group multiple tools and simplify their collective registration and management. Useful for modularizing agent capabilities.
    - name: "Dependency Injection"
      description: |
        Allows agent context or other dependencies to be automatically provided to tool functions, supporting composability and extensibility.
    - name: "Tool Interoperability"
      description: |
        Enables tools from other ecosystems (e.g., LangChain, CrewAI) to be converted and registered as native tools via the interoperability protocol and registry.
    - name: "GroupChat and Group Patterns"
      description: |
        In group agent settings, tool registration and execution must be coordinated to ensure all relevant agents have access to the necessary tools.
    - name: "LLMConfig"
      description: |
        LLMConfig impacts which models support function-calling, and thus whether registered tools are accessible to the LLM for proposal. Agents should be configured with compatible model settings.