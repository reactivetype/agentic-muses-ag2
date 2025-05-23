# Integrating New LLM Providers


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Accuracy"
      description: "The examples imply that simply registering a custom LLMConfigEntry and client is sufficient for agent integration, but do not specify how the framework discovers and uses the new client (e.g., agent expects a standard client interface, but there is no explicit registration of the client)."
      severity: "medium"
      suggestion: "Clarify how the agent is wired to use the custom SuperLLMClient. If a factory or registry is required, or if the config entry must specify the client, add this detail."
    - type: "Completeness"
      description: "Authentication and error handling in the code samples are minimal; the sample client does not demonstrate robust error handling, timeouts, or retries."
      severity: "medium"
      suggestion: "Add a brief note or code comment advising users to implement proper error handling and authentication management in real-world clients."
    - type: "Clarity"
      description: "The relationship between LLMConfigEntry and the client is not clearly explained; a new user may be unclear if/when they need to subclass both or how the wiring works."
      severity: "low"
      suggestion: "Add a diagram or short section explaining how LLMConfigEntry and the provider client interact and how agents connect with them."
    - type: "Code Example Quality"
      description: "In the 'Provider-Specific Tool Calling' example, the code is incomplete ('# ... send API request and handle response') and does not show a working end-to-end example."
      severity: "medium"
      suggestion: "Either provide a more complete example or state explicitly that only the relevant snippet is shown, and reference the first example for full integration."
    - type: "Best Practices"
      description: "While best practices are listed, there is no explicit mention of versioning, backward compatibility, or how to handle breaking changes in provider APIs."
      severity: "low"
      suggestion: "Add a best practice bullet about considering API versioning and deprecation policies for custom providers."
  strengths:
    - "Clear structure: Overview, explanation, examples, best practices, and related concepts are well organized and separated."
    - "Code examples are practical and directly related to the integration tasks users will perform."
    - "Best practices section is actionable and covers common pitfalls (compatibility, authentication, testing)."
    - "Related concepts are succinctly described, guiding users to broader framework understanding."
  recommendations:
    - "Clarify the mechanism by which agents discover and use the custom LLM client; add a note or example if a factory, registry, or interface adherence is required."
    - "Improve code samples by including basic error handling and clarifying incomplete snippets to avoid confusion."
    - "Enhance the explanation of how LLMConfigEntry and the client interact, potentially with a diagram or flow description."
    - "Add a note in best practices about handling provider API changes and versioning."
```


## Content

```yaml
content:
  overview: |
    Integrating new Large Language Model (LLM) providers allows you to extend the framework to support custom or third-party APIs beyond the built-in options (e.g., OpenAI, Azure, Gemini). By implementing provider-specific configuration and client logic, you enable agents and toolchains to interact with additional LLM backends in a unified, interoperable manner.

  explanation: |
    The framework uses standardized abstractions—such as `LLMConfig`, `LLMConfigEntry`, and agent protocols—to decouple agent logic from specific LLM providers. To add support for a new LLM or API backend:

    1. **Define a Provider-Specific LLMConfigEntry:**  
       Subclass `LLMConfigEntry` to represent your provider's model configuration (API endpoint, key, parameters, etc.). This ensures consistent validation and serialization.

    2. **Implement a Provider Client:**  
       Create a client class responsible for sending requests to your LLM provider, parsing responses, and handling errors. This client should conform to the expected interface (e.g., a `generate()` or `complete()` method).

    3. **Register with LLMConfig:**  
       Your new `LLMConfigEntry` should be registered within an `LLMConfig` object, allowing agents and group managers to select and use your backend seamlessly.

    4. **Integrate with Agents:**  
       Pass your custom config to agents (e.g., `ConversableAgent`) via their `llm_config` parameter. Agents and toolkits will then use your backend for all LLM calls.

    This design enables features like context management, filtering, and group orchestration to work with any compliant LLM provider, fostering extensibility and maintainability.

  examples:
    - title: "Basic Integration of a Custom LLM Provider"
      description: |
        This example shows how to add a new provider called `SuperLLM` by defining a config entry and a simple client.
      code: |
        # 1. Define the provider-specific config entry
        from autogen.llm_config import LLMConfigEntry

        class SuperLLMConfigEntry(LLMConfigEntry):
            def __init__(self, api_url: str, api_key: str, model: str, **kwargs):
                super().__init__(provider="superllm", model=model, **kwargs)
                self.api_url = api_url
                self.api_key = api_key

        # 2. Implement the provider client
        class SuperLLMClient:
            def __init__(self, config: SuperLLMConfigEntry):
                self.config = config
            def generate(self, prompt, **kwargs):
                import requests
                headers = {"Authorization": f"Bearer {self.config.api_key}"}
                data = {"model": self.config.model, "prompt": prompt}
                resp = requests.post(f"{self.config.api_url}/v1/generate", json=data, headers=headers)
                return resp.json()["result"]

        # 3. Register and use with an agent
        from autogen import ConversableAgent
        config_entry = SuperLLMConfigEntry(api_url="https://api.superllm.com", api_key="sk-xxx", model="super-1")
        llm_config = LLMConfig([config_entry])
        agent = ConversableAgent("super_agent", llm_config=llm_config)
        response = agent.receive("Hello, SuperLLM!")
    - title: "Provider-Specific Tool Calling"
      description: |
        Demonstrates how to enable function/tool calling with a new LLM provider by ensuring your client supports the function-calling protocol.
      code: |
        class SuperLLMClient:
            def __init__(self, config):
                self.config = config
            def generate(self, prompt, tools=None, **kwargs):
                payload = {"prompt": prompt, "model": self.config.model}
                if tools:
                    payload["tools"] = [tool.to_openai_schema() for tool in tools]
                # ... send API request and handle response

        # Register tools as usual
        from autogen.tools import tool

        @tool(name="multiply", description="Multiply two numbers")
        def multiply(a: int, b: int) -> int:
            return a * b

        agent.register_for_llm()(multiply)
  best_practices:
    - "Follow the LLMConfigEntry abstraction for all provider-specific settings to ensure compatibility."
    - "Reuse existing client patterns (e.g., OpenAIClient) as templates for your custom client class."
    - "Validate that your provider supports required features (e.g., streaming, function calling) before exposing them to agents."
    - "Document authentication and environment variable requirements for users."
    - "Test integration in both single-agent and group chat scenarios to catch edge cases."
    - "Leverage LLMConfig context management to minimize config boilerplate and avoid state leakage."
  related_concepts:
    - name: "LLMConfig and LLMConfigEntry"
      description: "These abstractions standardize provider config and ensure agents can select between multiple backends."
    - name: "ConversableAgent and Agent Protocols"
      description: "Agents use the llm_config parameter to determine which LLM backend to use for message generation and tool calling."
    - name: "Tool and Toolkit"
      description: "Tool registration works uniformly regardless of LLM provider, provided the client supports the function-calling protocol."
    - name: "GroupChat and Patterns"
      description: "Group orchestrations can utilize any LLM provider registered via LLMConfig, enabling flexible multi-agent setups."
    - name: "Tool Interoperability"
      description: "Custom LLM providers can interoperate with tools from other ecosystems if tool schemas are respected."
```