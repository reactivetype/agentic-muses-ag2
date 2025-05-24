# LLM Configuration


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Accuracy and Technical Correctness"
      description: "The documentation refers to methods like `LLMConfig.from_json(env=...)` and `LLMConfig.from_env`, but only `from_json` is shown in use. If both exist, their differences should be clarified. Also, provider-specific subclass examples are limited to OpenAI; Azure and Gemini are mentioned in the overview but not exemplified."
      severity: "medium"
      suggestion: "Clarify availability and differences between `from_json` and `from_env`. Add at least one example or mention for Azure/Gemini configuration."

    - type: "Clarity and Readability"
      description: "Some sentences are dense and could benefit from clearer structure or simpler language. For example, the explanation of context management and the relationship between LLMConfig and agents can be more concise."
      severity: "low"
      suggestion: "Split long sentences, and use bullet points or subheadings where appropriate for easier reading."

    - type: "Completeness and Comprehensiveness"
      description: "The best practices and examples do not address error handling, troubleshooting, or how to extend LLMConfigEntry for new providers."
      severity: "medium"
      suggestion: "Add a note or example about error handling, and briefly mention how to extend for unsupported providers."

    - type: "Code Example Quality"
      description: "Most code examples are clear, but they lack comments explaining the rationale for each step, and do not show the output or expected results. Also, some imports are inconsistent (e.g., `from autogen.oai.client import OpenAILLMConfigEntry`—should this be directly accessible?)."
      severity: "low"
      suggestion: "Add inline comments to code, and clarify import paths if needed. Optionally, show expected output for at least one example."

    - type: "Best Practices Coverage"
      description: "Best practices are good but could include advice on managing credentials securely (e.g., using secrets managers over environment variables in production), and on testing LLM configurations."
      severity: "low"
      suggestion: "Expand best practices to include credential management and testing recommendations."
  strengths:
    - "Very thorough overview that explains both high-level concepts and practical details of LLM configuration."
    - "Examples cover initialization, provider-specific configuration, context management, and filtering, demonstrating the core workflow."
  recommendations:
    - "Add or reference an example for non-OpenAI providers (Azure, Gemini) to demonstrate multi-provider support."
    - "Clarify and differentiate between `from_json` and `from_env` methods, and include a note on how to extend for additional providers."
```


## Content

```yaml
content:
  overview: |
    LLM Configuration is the foundational process of specifying, validating, and managing the settings required to use large language models (LLMs) and their clients within the agent framework. This includes selecting providers (e.g., OpenAI, Azure, Gemini), defining model parameters, handling authentication, and orchestrating model usage across agents and groups. Robust LLM configuration ensures agents can communicate effectively, leverage advanced features such as tool calling, and operate securely in multi-agent or multi-provider environments.
  explanation: |
    Configuring an LLM involves more than just providing an API key and model name. The framework introduces the `LLMConfig` and `LLMConfigEntry` abstractions to standardize configuration for all supported LLM providers. This design enables agents, toolkits, and group orchestrations to interact with LLMs in a provider-agnostic way, supporting serialization, filtering, context management, and extensibility.

    - **LLMConfig**: Represents a collection of `LLMConfigEntry` objects, each specifying the configuration for a single model/provider. It supports loading from JSON files, environment variables, or direct instantiation, and provides filtering and context management for advanced use cases.
    - **LLMConfigEntry**: An abstract base class for individual model configurations (e.g., model name, API key, endpoint). Each provider (such as OpenAI, Azure, Gemini) has its own subclass with required fields.
    - **Context Management**: Using `LLMConfig.current(...)` as a context manager allows for temporary overriding of the active configuration, useful in multi-threaded or multi-agent scenarios.

    Agents, such as those inheriting from `ConversableAgent`, are initialized with an `llm_config` parameter. This ensures that all agent operations, including tool-calling and message generation, are governed by the specified model configuration. Advanced usage includes filtering configurations for specific models or capabilities, and leveraging environment-based loading for secure and scalable deployments.

    Proper LLM configuration is essential for:
    - Ensuring consistent, secure, and reproducible agent behavior.
    - Switching between providers or models without code changes.
    - Supporting advanced features like function-calling, chat history management, and group orchestration.
  examples:
    - title: "Basic Agent Setup with LLMConfig"
      description: "Initialize a ConversableAgent with an LLM configuration loaded from environment variables."
      code: |
        from autogen.llm_config import LLMConfig
        from autogen import ConversableAgent

        # Load configuration from an environment variable (e.g., OAI_CONFIG_LIST)
        config = LLMConfig.from_json(env="OAI_CONFIG_LIST")

        # Create an agent with the loaded config
        agent = ConversableAgent(
            name="assistant",
            system_message="You are a helpful AI.",
            llm_config=config
        )
    - title: "Provider-Specific Configuration"
      description: "Directly specify an OpenAI model and API key using OpenAILLMConfigEntry."
      code: |
        from autogen.oai.client import OpenAILLMConfigEntry
        from autogen.llm_config import LLMConfig
        from autogen import ConversableAgent

        entry = OpenAILLMConfigEntry(
            model="gpt-4",
            api_key="sk-...",
            organization="org-..."
        )
        config = LLMConfig([entry])
        agent = ConversableAgent("openai_agent", llm_config=config)
    - title: "Context Management for Temporary LLMConfig"
      description: "Temporarily override the global LLM configuration within a code block."
      code: |
        from autogen.llm_config import LLMConfig

        config = LLMConfig.from_json(env="OAI_CONFIG_LIST")
        with LLMConfig.current(config):
            # All agents created here will use 'config' unless specifically overridden
            ...
    - title: "Filtering LLMConfig for a Specific Model"
      description: "Select only GPT-4 entries from a multi-provider configuration list."
      code: |
        config = LLMConfig.from_json(env="OAI_CONFIG_LIST")
        gpt4_config = config.where(model="gpt-4")
        agent = ConversableAgent("gpt4_agent", llm_config=gpt4_config)
  best_practices:
    - "Always use provider-specific LLMConfigEntry subclasses for correct field validation."
    - "Load configurations from secure sources (environment variables, secrets managers), not hardcoded values."
    - "Use `LLMConfig.from_json` or `from_env` for scalable, environment-driven deployments."
    - "Filter LLMConfig with `.where()` to target specific models or providers for agents."
    - "Leverage context management (`with LLMConfig.current(...)`) for temporary changes, especially in testing or multi-agent workflows."
    - "Avoid passing raw dictionaries as `llm_config`; always use LLMConfig for consistency and validation."
  related_concepts:
    - name: "ConversableAgent (and Agent Protocols)"
      description: "Agents require `llm_config` to communicate with LLMs and perform message generation and tool-calling."
    - name: "Tool and Toolkit"
      description: "LLM configuration affects which tools can be invoked by the agent, especially for function-calling models."
    - name: "GroupChat and Group Patterns"
      description: "Group chat orchestration may require consistent or per-agent LLMConfig for coordinated conversations."
    - name: "LLMConfigEntry"
      description: "Represents individual model/provider configurations used within LLMConfig."
    - name: "Context Management"
      description: "Contextual configuration enables safe overrides and multi-threaded agent scenarios."
```