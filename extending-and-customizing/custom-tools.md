# Custom Tools


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The documentation does not specify the full import path for ConversableAgent, which may confuse users if autogen is modularized. Also, some agent registration methods (like .register_tool) are shown but not explained."
      severity: "medium"
      suggestion: "Clarify all import paths and briefly explain the differences between registration methods."
    - type: "Completeness"
      description: "Does not mention how to unregister or update tools, nor does it discuss error handling when a tool fails."
      severity: "medium"
      suggestion: "Add a section or note on tool lifecycle management (unregister/update) and error handling best practices."
    - type: "Clarity"
      description: "The explanation of interoperability with external tools is brief and lacks a concrete example for CrewAI."
      severity: "low"
      suggestion: "Expand the interoperability section with more detailed examples or references."
    - type: "Code Example Quality"
      description: "Some registration code is out of context or ambiguous (e.g., agent.register_for_llm()(add_employee) assumes agent exists, but not fully shown in that example)."
      severity: "low"
      suggestion: "Ensure all code snippets are self-contained or clarify prerequisites in comments."
    - type: "Best Practices Coverage"
      description: "While most best practices are covered, there is no mention of tool documentation/testing or security considerations."
      severity: "low"
      suggestion: "Add best practices around testing tools and security (e.g., avoiding unsafe operations in tools)."
  strengths:
    - "Clear and thorough explanation of the core concept and workflow for custom tools."
    - "Good range of code examples, including basic usage, grouping, complex input, and interoperability."
    - "Best practices are practical and actionable."
    - "Related concepts section effectively links to other parts of the agent framework."
  recommendations:
    - "Add a short section on unregistering/updating tools and handling tool errors."
    - "Expand on interoperability with additional examples and clarify import paths and registration methods."
    - "Ensure all code examples are either fully runnable or include comments on required setup."
    - "Consider adding a tip or warning box about security and validation, especially when exposing tool logic to LLMs."
```


## Content

```yaml
content:
  overview: |
    Custom tools allow you to extend agent capabilities by defining your own functions that agents can call during conversations. By building and integrating custom tools, you enable agents to perform specific tasks, interact with external systems, and provide richer, more actionable responses. The framework provides abstractions and decorators for defining, registering, and managing custom tools, ensuring seamless function-calling by LLMs and agents.
  explanation: |
    In the agent framework, "tools" are lightweight wrappers around Python callables (functions, methods, or objects) that expose their signature and description to both agents and LLMs. This enables LLMs to propose tool usage (function calls) during conversations, and lets agents execute these tools as part of their workflow.

    You can create a custom tool by:
      - Writing a Python function with clear type annotations and a docstring or description.
      - Decorating the function with the `@tool` decorator (from `autogen.tools`) to mark it as a Tool.
      - Registering the tool with an agent (using `.register_tool`, `.register_for_llm`, or `.register_for_execution`).
      - Optionally grouping tools using a `Toolkit` for collective management and registration.
    
    Once registered, tools become available to the agent’s LLM for function-calling and/or direct execution. This allows the agent to invoke your custom logic in response to user queries or during multi-agent workflows.

    The system supports interoperability with external tool ecosystems (like LangChain or CrewAI) via converters, but the recommended pattern is to use the provided abstractions for native tool development. For complex parameter schemas, Pydantic models can be used for input validation.

    Tool registration is compositional: agents and toolkits can hold and manage multiple tools, and tools must be registered before initiating chats to ensure visibility for LLM function-calling.

  examples:
    - title: "Defining and Registering a Simple Custom Tool"
      description: "Create an addition tool and register it for LLM function-calling."
      code: |
        from autogen.tools import tool
        from autogen import ConversableAgent

        @tool(name="add", description="Add two numbers together.")
        def add(a: int, b: int) -> int:
            """Adds two integers and returns the result."""
            return a + b

        agent = ConversableAgent(
            name="calculator",
            system_message="You are a math assistant.",
            llm_config={...}
        )

        agent.register_for_llm()(add)  # Make tool available for LLM function calling

        # Now, when chatting with the agent, the LLM can propose using 'add'
    - title: "Grouping Multiple Tools with a Toolkit"
      description: "Bundle related tools and register them collectively."
      code: |
        from autogen.tools import tool, Toolkit

        @tool(name="multiply", description="Multiply two numbers.")
        def multiply(a: int, b: int) -> int:
            return a * b

        @tool(name="subtract", description="Subtract two numbers.")
        def subtract(a: int, b: int) -> int:
            return a - b

        math_toolkit = Toolkit([multiply, subtract])
        math_toolkit.register_for_llm(agent)  # Register all tools in the toolkit

    - title: "Custom Tool with Complex Input Using Pydantic"
      description: "Define a tool that validates its input using a Pydantic model."
      code: |
        from pydantic import BaseModel
        from autogen.tools import tool

        class Employee(BaseModel):
            name: str
            age: int
            department: str

        @tool(name="add_employee", description="Add an employee record.")
        def add_employee(employee: Employee) -> str:
            # Save employee to database (stub)
            return f"Added employee: {employee.name}"

        agent.register_for_llm()(add_employee)

    - title: "Registering a Tool for Direct Execution (By Agent)"
      description: "Allow an agent to execute a tool directly, not just propose via LLM."
      code: |
        agent.register_for_execution()(add)  # Agent can execute 'add' directly in its logic

    - title: "Converting External Tools (Interoperability)"
      description: "Convert a LangChain or CrewAI tool for use as an agent tool."
      code: |
        from autogen.tools.interop import Interoperability

        # Assume langchain_tool is an instance of a LangChain tool
        ag2_tool = Interoperability.convert_tool(langchain_tool)
        agent.register_tool(ag2_tool)

  best_practices:
    - "Use the @tool decorator to define tools; avoid manual Tool construction for clarity and introspection."
    - "Provide clear, concise descriptions and accurate type annotations for all tool parameters."
    - "Register tools with agents before starting any chat; unregistered tools won’t be visible to LLMs."
    - "Group related tools in a Toolkit for easier management and registration."
    - "For complex input validation, use Pydantic models as input parameters."
    - "Avoid side effects or long-running operations in tools unless required; tools should be fast and reliable."
    - "Keep tool logic independent and stateless when possible for composability and testability."

  related_concepts:
    - name: "ConversableAgent and Agent Protocols"
      description: "Agents are the primary consumers of tools; tools must be registered with an agent for LLM function-calling or execution."
    - name: "Toolkit"
      description: "Toolkits bundle multiple tools for collective management and registration with agents."
    - name: "Tool Interoperability"
      description: "The interoperability layer allows you to convert tools from other ecosystems (LangChain, CrewAI, etc.) to be used as agent tools."
    - name: "LLMConfig"
      description: "Controls which LLM(s) your agent uses; some LLMs are better at function-calling and tool usage."
    - name: "GroupChat and Patterns"
      description: "In group settings, tools can be shared among agents or used in orchestrated workflows."
```
