# Function Utilities


## Quality Check

quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The documentation refers to 'autogen.tools' and AG2 Tool objects without clarifying the specific library or framework (e.g., Microsoft AutoGen, hypothetical AG2). This could confuse users if not in the intended context."
      severity: "medium"
      suggestion: "Clarify the library/framework being referenced at the beginning of the section."
    - type: "Clarity"
      description: "Some sentences in the overview and explanation are dense and could be broken up for easier readability, especially for less experienced users."
      severity: "low"
      suggestion: "Shorten sentences and use more bullet points for key concepts."
    - type: "Completeness"
      description: "Error handling and edge cases (e.g., what happens if parameter validation fails, or if type hints are missing) are not discussed."
      severity: "medium"
      suggestion: "Add a brief subsection or note about error handling and limitations."
    - type: "Code Example Quality"
      description: "The code examples are strong, but it's not always clear what the expected output is or how the schema looks in practice."
      severity: "low"
      suggestion: "For at least one example, include an actual sample output (or partial output) to illustrate what the schema looks like."
    - type: "Best Practices Coverage"
      description: "While the best practices listed are solid, they do not mention security or privacy considerations (e.g., avoiding exposing sensitive functions as tools)."
      severity: "low"
      suggestion: "Add a best practice about reviewing tool exposure for security/privacy."
  strengths:
    - "Thorough and technically detailed explanation of function utilities and their role in agentic frameworks."
    - "Diverse, practical code examples that illustrate simple, advanced, and real-world use cases."
    - "Clear separation of conceptual overview, best practices, and related concepts, making the document easy to navigate."
    - "Best practices section is actionable and relevant to both beginners and advanced users."
  recommendations:
    - "Clarify the library/framework context (e.g., Microsoft AutoGen, AG2) to avoid confusion."
    - "Add a brief discussion of error handling and common pitfalls when using function utilities."
    - "Include at least one example of a generated schema's actual output for illustrative purposes."
    - "Consider mentioning security/privacy best practices for tool exposure."


## Content

content:
  overview: |
    Function utilities are foundational to agentic frameworks, enabling agents to dynamically understand, expose, and invoke Python functions as "tools" for use by language models (LLMs) and other agents. Core aspects include automatic function schema generation (for parameter validation and tool descriptions) and robust function parameter management. These utilities ensure seamless agent-tool integration, safe execution, and compatibility with function-calling LLMs.

  explanation: |
    In agent-based systems, functions are often exposed as "tools" that agents (and LLMs) can call during conversations. To facilitate this, the system must generate a machine-readable "schema" for each function—describing its name, description, expected parameters (types, defaults), and return type. This schema is used for validation, tool registration, and LLM prompt generation (e.g., for OpenAI's function-calling API).

    The function utilities abstraction automates:
      - Parsing function signatures (using type hints and docstrings)
      - Serializing parameter schemas (to JSON Schema, OpenAPI, or other formats)
      - Handling optional/required parameters, defaults, and nested models (e.g., via Pydantic)
      - Registering functions as tools, associating metadata and schemas
      - Validating and converting inputs at call time

    These utilities underpin the "Tool" abstraction, ensuring that tools are described accurately and consistently, and that agents can reliably propose, validate, and execute tool calls. Proper function schema management is critical for interoperability (e.g., tool conversion between ecosystems), for LLM-driven function calling, and for robust agent behaviors.

  examples:
    - title: "Registering a Simple Function as a Tool"
      description: "Automatically generate a schema and expose a function for LLM/agent use."
      code: |
        from autogen.tools import tool

        @tool(name="add", description="Add two numbers together")
        def add(a: int, b: int) -> int:
            return a + b

        # The tool decorator auto-generates a schema:
        print(add.schema())
        # Output includes parameter types, required/optional fields, description

    - title: "Function with Default and Optional Parameters"
      description: "Showcase parameter management, including defaults and optionals."
      code: |
        @tool(name="greet", description="Greet a user, optionally with a custom message.")
        def greet(name: str, message: str = "Hello") -> str:
            return f"{message}, {name}!"

        # Parameter schema includes 'name' (required) and 'message' (optional, default="Hello")

    - title: "Complex Parameter Schema with Pydantic"
      description: "Handle structured/nested input using Pydantic models."
      code: |
        from pydantic import BaseModel
        from autogen.tools import tool

        class UserInfo(BaseModel):
            name: str
            age: int

        @tool(name="register_user")
        def register_user(user: UserInfo) -> str:
            return f"Registered {user.name}, age {user.age}"

        # The schema will reflect nested object structure for 'user'

    - title: "Inspecting and Validating Function Parameters"
      description: "Use schema info for runtime validation or UI generation."
      code: |
        tool_obj = add  # The decorated function is a Tool object
        print(tool_obj.schema())  # JSON schema for tool parameters

        # Validate input before calling:
        params = {"a": 5, "b": 7}
        validated = tool_obj.validate_parameters(params)
        result = tool_obj(**validated)  # Safe execution

  best_practices:
    - "Always annotate function parameters and return types for accurate schema generation."
    - "Provide clear, concise descriptions for each tool and its parameters—these aid both LLMs and human users."
    - "Use Pydantic models for complex or nested input parameters to leverage automatic validation and rich schemas."
    - "Prefer the @tool decorator for tool registration, as it ensures schema consistency and avoids manual errors."
    - "Register tools with agents before starting conversations, so LLMs have access to up-to-date tool schemas."
    - "Avoid using mutable default arguments or unsupported Python types in tool signatures."
    - "Test schema generation and parameter handling for each tool, especially when updating function signatures."

  related_concepts:
    - name: "Tool and Toolkit"
      description: "Function utilities form the basis for the Tool abstraction, which wraps functions (with schemas) for agent/LLM use."
    - name: "ConversableAgent"
      description: "Agents use function utilities to register, describe, and execute tools during conversations."
    - name: "Tool Interoperability"
      description: "Schema generation enables conversion of external tool formats (e.g., LangChain, CrewAI) into compatible AG2 Tool objects."
    - name: "LLM Function Calling"
      description: "Accurate function schemas are essential for LLMs to call functions/tools, validate arguments, and interpret return values."
    - name: "Pydantic Models"
      description: "Use Pydantic for complex parameter schemas; function utilities natively support Pydantic input models for tools."