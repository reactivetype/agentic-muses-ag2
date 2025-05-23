# Interoperability


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The documentation assumes the existence and interfaces of certain classes/methods (e.g., Interoperability.convert, InteroperableRegistry.register, AG2 Tool), but does not specify what AG2 refers to or whether these interfaces are stable/public."
      severity: "medium"
      suggestion: "Clearly define what 'AG2' stands for on first mention and briefly describe its Tool/Toolkit classes. Ensure referenced APIs exist and are public/stable."
    - type: "Clarity"
      description: "Some explanations are dense and use jargon (e.g., 'first-class citizens', 'LLM function-calling') that may not be familiar to all readers."
      severity: "medium"
      suggestion: "Add brief explanations or links to jargon-heavy terms; consider a glossary or parenthetical clarifications."
    - type: "Completeness"
      description: "Edge cases and potential conversion pitfalls (e.g., parameter schema mismatches, error handling if conversion fails) are not discussed."
      severity: "medium"
      suggestion: "Add a troubleshooting or 'Limitations' subsection to highlight known pitfalls and how to handle failed conversions or mismatches."
    - type: "Code Example Quality"
      description: "Code examples do not include error handling or checks for conversion success, and some objects (e.g., agent, llm_config, my_special_tool_instance) are assumed to exist without definition."
      severity: "low"
      suggestion: "Add minimal definitions or comments for assumed objects, and optionally show basic error handling or validation after conversion."
    - type: "Best Practices"
      description: "Best practices are comprehensive but could emphasize version compatibility and security risks when integrating third-party tools."
      severity: "low"
      suggestion: "Add best practices on checking version compatibility and reviewing external tool code for security."
  strengths:
    - "Clear high-level overview of the interoperability mechanism and its benefits."
    - "Well-structured, practical code examples that illustrate the main use cases."
    - "Comprehensive list of best practices and related concepts for further learning."
    - "Step-by-step explanations of the conversion process and extensibility."
  recommendations:
    - "Define all acronyms and key classes/interfaces on first use to aid newcomers."
    - "Expand on error handling and troubleshooting for conversion failures or incompatibilities."
    - "Improve code examples by clarifying assumed context and demonstrating minimal input setup and error management."
    - "Consider adding a diagram of the interoperability flow for visual learners."
```


## Content

```yaml
content:
  overview: |
    Interoperability in agent frameworks allows you to leverage tools and utilities from external ecosystems—such as LangChain, CrewAI, or Pydantic-AI—within your own agent workflows. This capability ensures that agents can use a unified tool abstraction, regardless of the original source or format of the tool, thus promoting code reuse and seamless integration across different libraries and communities.

  explanation: |
    The agent framework provides a structured approach to tool interoperability, making it possible to import, convert, and utilize tools from various external sources as first-class citizens in agent conversations. This is achieved through a combination of protocols, registries, and conversion utilities:

    - **Interoperable Protocol:** Any external tool or toolkit can be made interoperable by adhering to a protocol that defines a `convert_tool()` method. This method is responsible for transforming the external tool into a standard AG2 `Tool` object with the required metadata (name, description, parameter schema, etc.).
    - **InteroperableRegistry:** The registry maintains a mapping of supported external tool types and their corresponding converters. New external tool types can be registered, enabling extensibility as new ecosystems emerge.
    - **Interoperability Facade:** The main interface (often `Interoperability.convert()`) detects the tool's origin, consults the registry, and applies the correct conversion logic, returning a usable `Tool` or `Toolkit` for agents.

    This design abstracts away ecosystem-specific details, letting you register and use tools from different frameworks exactly as you would native tools. For example, you can import a LangChain tool or a CrewAI tool, convert it, and register it with your agent, making it available for LLM function-calling or direct invocation.

    Common conversion points include:
      - Wrapping LangChain's `Tool` or `Toolkit` objects for AG2 agent usage
      - Translating CrewAI tool schemas into the AG2 tool format
      - Converting Pydantic-AI functions or models into AG2 tools

    This approach ensures that your agent ecosystem stays flexible and future-proof, able to incorporate innovations and capabilities from the broader AI tooling community.

  examples:
    - title: "Importing and Converting a LangChain Tool"
      description: "Convert a LangChain tool to an AG2 Tool and register it with an agent."
      code: |
        from langchain.tools import Tool as LangChainTool
        from autogen.tools.interoperability import Interoperability
        from autogen import ConversableAgent

        # Assume you have a LangChain tool
        def multiply(a: int, b: int) -> int:
            return a * b
        lc_tool = LangChainTool(
            name="Multiply",
            func=multiply,
            description="Multiply two numbers"
        )

        # Convert LangChain tool to AG2 Tool
        ag2_tool = Interoperability.convert(lc_tool)

        # Register with agent
        agent = ConversableAgent("assistant", llm_config={...})
        agent.register_tool(ag2_tool)
    - title: "Batch Conversion: CrewAI Toolkit"
      description: "Convert all tools in a CrewAI toolkit and register as a group with an agent."
      code: |
        from crewai.tools import Toolkit as CrewAIToolkit
        from autogen.tools.interoperability import Interoperability
        from autogen.tools import Toolkit

        # CrewAI toolkit with several tools
        crewai_toolkit = CrewAIToolkit([...])

        # Convert CrewAI toolkit to AG2 Toolkit
        ag2_toolkit = Interoperability.convert(crewai_toolkit)

        # Register all tools for agent LLM access
        ag2_toolkit.register_for_llm(agent)
    - title: "Custom Converter Registration"
      description: "Support a new external tool type by registering a custom converter."
      code: |
        from my_external_lib import MySpecialTool
        from autogen.tools.interoperability import InteroperableRegistry

        class MySpecialToolConverter:
            @staticmethod
            def convert_tool(obj):
                # Custom logic to wrap MySpecialTool as AG2 Tool
                return Tool(
                    name=obj.display_name,
                    description=obj.summary,
                    function=obj.callable,
                    parameter_schema=obj.schema
                )

        # Register custom converter for MySpecialTool
        InteroperableRegistry.register(MySpecialTool, MySpecialToolConverter)

        # Now convertible via Interoperability.convert()
        ag2_tool = Interoperability.convert(my_special_tool_instance)

  best_practices:
    - "Always provide accurate metadata (name, description, type hints) in your external tools to ensure seamless conversion."
    - "Prefer using the official Interoperability facade instead of writing ad-hoc conversion code."
    - "Test converted tools individually before deploying them in multi-agent or production settings."
    - "Be mindful of parameter schema differences between ecosystems; use Pydantic models for complex types."
    - "Register new external tool converters with the InteroperableRegistry to enable automatic conversion for your team or project."
    - "Keep tool dependencies lightweight and ensure that any required external libraries are installed in your environment."

  related_concepts:
    - name: "Tool and Toolkit"
      description: "The unified abstraction that all converted external tools must conform to, ensuring consistent registration and invocation."
    - name: "ConversableAgent"
      description: "The agent interface that uses registered tools, including those imported from other ecosystems via interoperability."
    - name: "Tool Registration"
      description: "The process by which tools (native or converted) are made accessible to agents and LLMs for function-calling."
    - name: "LLMConfig"
      description: "Ensures that the LLMs used by agents are properly configured to recognize and invoke registered tools, including those converted from other ecosystems."
    - name: "GroupChat and Patterns"
      description: "Converted tools can be shared among multiple agents participating in group chat orchestrations."
```