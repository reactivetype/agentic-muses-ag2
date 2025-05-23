# Testing Patterns


## Quality Check

quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The section gives an accurate overview of testing abstractions within the agent framework. However, some code examples may oversimplify real agent-tool interaction, particularly how tools are invoked during conversations (e.g., agent.generate_reply may not trigger tool execution without proper message parsing)."
      severity: "medium"
      suggestion: "Clarify in the integration example how tool invocation is handled, or provide a more realistic example of agent-tool interaction that demonstrates the tool being called and a mocked result being returned."
    - type: "Completeness"
      description: "Limited coverage of negative/error-path testing in the examples, though it's mentioned in best practices."
      severity: "medium"
      suggestion: "Add at least one example covering error handling or negative testing scenarios, such as registration of an invalid tool or failed orchestration."
    - type: "Clarity"
      description: "Some terms (e.g., 'protocol compliance', 'tool wrapping') are used without definition, which may confuse new users."
      severity: "low"
      suggestion: "Briefly define less common terms or link to further documentation upon first use."
    - type: "Code Example Quality"
      description: "Examples are clear and runnable, but some (like LLM mocking) may not reflect full conversational logic or don't show assertions for side effects (e.g., tool call count)."
      severity: "low"
      suggestion: "Enhance code examples with additional assertions or comments to clarify what is being tested and expected outcomes."
  strengths:
    - "Excellent structure and logical flow, moving from overview to explanation, then to concrete examples and best practices."
    - "Comprehensive listing of test targets and best practices relevant to asynchronous, multi-agent systems."
    - "Examples are concise and demonstrate key points (unit, integration, orchestration, config parsing)."
    - "Best practices section is actionable and relevant for real-world agentic frameworks."
  recommendations:
    - "Expand examples to include at least one negative or error-path test (e.g., ensuring an exception is raised for invalid tool registration)."
    - "Clarify or link terms that may not be familiar to all readers, enhancing accessibility."
    - "In integration examples, better demonstrate actual tool invocation, perhaps by asserting tool call effects or by mocking the entire tool chain."
    - "Consider adding a brief section or inline notes on how to extend these patterns for more complex or custom orchestration scenarios."


## Content

content:
  overview: |
    Testing Patterns encompass strategies and approaches for ensuring comprehensive test coverage of agent, tool, group chat, and core utility abstractions within the framework. By systematically applying appropriate testing techniques, developers can validate the correctness, reliability, and integration of complex agentic behaviors, orchestration patterns, and utility modules.
  explanation: |
    The agent framework's modular and extensible design—spanning agents, tools, group chat orchestrations, and configuration utilities—necessitates robust testing methodologies. Testing Patterns refer to the set of practices and patterns employed to verify both individual components and their collaborations, including:
    
    - **Unit Testing**: Isolating and testing single components (e.g., a tool function or an agent's message handler).
    - **Integration Testing**: Validating interactions among multiple components (e.g., agent-tool registration, group chat workflows).
    - **End-to-End Testing**: Simulating real-world scenarios (e.g., a full chat session with tool usage and group transitions).
    - **Mocking and Stubbing**: Using mocks for LLM responses or external APIs to ensure deterministic tests.
    - **Test Utilities**: Leveraging built-in test helpers (e.g., mock agents, dummy LLM configs) for setup and teardown.
    
    High test coverage is critical due to the asynchronous, multi-agent, and tool-executing nature of the framework. Test suites should target:
    
    - **ConversableAgent and Agent Protocols**: Message flow, tool registration, chat history, and protocol compliance.
    - **Tool and Toolkit**: Tool wrapping, registration, execution, and interoperability.
    - **GroupChat Patterns**: Orchestration logic, speaker selection, transitions, and group manager workflows.
    - **LLMConfig and Utilities**: Configuration parsing, context management, and filtering.
    
    This ensures that both individual features and their combinations behave as intended and can be maintained as the codebase evolves.
  examples:
    - title: "Unit Testing a Tool Registration on an Agent"
      description: "Verifies that a tool function is correctly registered and callable via the agent."
      code: |
        import pytest
        from autogen import ConversableAgent
        from autogen.tools import tool

        @tool(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        def test_tool_registration():
            agent = ConversableAgent("test_agent")
            agent.register_tool(add)
            assert "add" in agent.list_tools()
    - title: "Integration Test: Agent Using a Tool in a Chat"
      description: "Tests that an agent can use a registered tool during conversation, using a mock LLM."
      code: |
        from autogen import ConversableAgent
        from autogen.tools import tool

        class DummyLLM:
            def generate_reply(self, *args, **kwargs):
                return {"content": "I will use the add tool."}

        @tool(name="add", description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        def test_agent_tool_usage(monkeypatch):
            agent = ConversableAgent("agent", llm_config={"llm": DummyLLM()})
            agent.register_tool(add)

            # Simulate a chat that would trigger tool usage
            response = agent.generate_reply("Please add 2 and 3")
            assert response["content"] == "I will use the add tool."
    - title: "Testing GroupChat Speaker Selection"
      description: "Ensures group chat transitions control correctly based on the orchestration pattern."
      code: |
        from autogen import GroupChat, GroupChatManager, ConversableAgent
        from autogen.agentchat.group.patterns.round_robin import RoundRobinPattern

        def test_groupchat_round_robin():
            a1 = ConversableAgent("a1")
            a2 = ConversableAgent("a2")
            pattern = RoundRobinPattern(initial_agent=a1, agents=[a1, a2])

            groupchat, manager = pattern.prepare_group_chat(max_rounds=2, messages=[])
            assert groupchat.speaker == a1
            groupchat.advance_round()
            assert groupchat.speaker == a2
    - title: "Testing LLMConfig Entry Parsing"
      description: "Checks that LLMConfig correctly parses and filters provider-specific configuration entries."
      code: |
        from autogen.llm_config import LLMConfig
        from autogen.oai.client import OpenAILLMConfigEntry

        def test_llm_config_parsing():
            entry = OpenAILLMConfigEntry(model="gpt-4", api_key="test")
            config = LLMConfig([entry])
            assert config.where(model="gpt-4")[0].model == "gpt-4"
  best_practices:
    - "Structure tests by abstraction: separate agent, tool, group, and utility tests."
    - "Use mocking for LLM or external service calls to ensure test determinism and speed."
    - "Test both positive (expected use) and negative (error/failure) scenarios."
    - "Leverage test fixtures for reusable setup of agents, tools, and group chats."
    - "Ensure coverage of custom orchestration logic and transitions in group chat patterns."
    - "Check serialization/deserialization and context management in utility tests."
    - "Continuously run tests in CI pipelines to detect regressions early."
    - "Document intent of complex integration tests for future maintainability."
  related_concepts:
    - name: "ConversableAgent (and Agent Protocols)"
      description: "Testing patterns start with agent abstractions, validating message flow, protocol adherence, and tool integration."
    - name: "Tool and Toolkit"
      description: "Unit and integration tests verify tool wrapping, registration, execution, and agent-tool interactions."
    - name: "GroupChat and Group Patterns"
      description: "Integration and end-to-end tests focus on group orchestration, speaker selection, and transition logic."
    - name: "LLMConfig and Utilities"
      description: "Utility testing ensures proper config parsing, filtering, and context management."
    - name: "Mocking and Test Utilities"
      description: "Mocks, stubs, and fixtures are essential for simulating LLMs and isolating test cases."
    - name: "Tool Interoperability"
      description: "Tests validate conversion and registration of external tools, ensuring interoperability contracts are met."