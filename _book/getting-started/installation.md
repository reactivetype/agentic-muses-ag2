# Installation


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Technical Accuracy"
      description: "The installation command for extras uses pip install autogen[group,langchain,toolkit], but pip sometimes requires quotes for extras (e.g., pip install 'autogen[group,langchain,toolkit]'). The syntax may not work on all shells/platforms."
      severity: "medium"
      suggestion: "Add a note or use quotes in the pip install command for extras to improve cross-platform compatibility."

    - type: "Clarity"
      description: "The section references abstractions (ConversableAgent, Tool, GroupChat, LLMConfig) before introducing or briefly explaining them, which could confuse newcomers."
      severity: "medium"
      suggestion: "Add a short introductory sentence or parenthetical definitions for each abstraction when first mentioned."

    - type: "Completeness"
      description: "No troubleshooting guidance is given if installation fails, and there is no explicit mention of supported Python versions or system requirements."
      severity: "medium"
      suggestion: "Add a short note on prerequisites (Python version, OS support) and a pointer for troubleshooting common installation issues."

    - type: "Code Example Quality"
      description: "The minimal agent test code is split between a one-liner and a multi-line example, but the latter lacks context that it’s expected to be run in a Python REPL or script, and may confuse users unfamiliar with Python."
      severity: "low"
      suggestion: "Clarify how/where to run the code (as a script or in the REPL), and consider adding expected output for confirmation."

    - type: "Best Practices"
      description: "The recommendation to use virtual environments is good, but the documentation does not show how to create or activate one."
      severity: "low"
      suggestion: "Include a brief example of creating and activating a virtual environment."

  strengths:
    - "Comprehensive coverage of installation paths, including optional dependencies and development versions."
    - "Clear, well-structured code examples that are generally easy to follow."
    - "Highlights the importance of environment variable setup for API keys and config."
    - "Best practices section is helpful and actionable."

  recommendations:
    - "Add a short section on prerequisites and troubleshooting to improve completeness."
    - "Use quotes in pip install commands for extras to improve compatibility."
    - "Provide brief one-line explanations or links for core abstractions when first mentioned."
    - "Show how to create/activate a virtual environment in the best practices or examples."
    - "Clarify where to run code examples and what output to expect, especially for beginners."
```


## Content

```yaml
content:
  overview: |
    Installation is the first step to getting started with the project. This section guides you through installing the core package, configuring dependencies, and verifying your setup, ensuring you are ready to build, configure, and run agent-based applications using the framework's abstractions like ConversableAgent, Tool, GroupChat, and LLMConfig.

  explanation: |
    The project supports flexible agentic communication, tool integration, group orchestration, and LLM management. To unlock these capabilities, you need to install the core package and configure any required dependencies (e.g., LLM provider access, API keys, and optional toolkits). Installation is usually done via pip, but certain features (like group orchestration or interoperability) may require extra dependencies.

    After installation, you should verify the installation by importing key modules and running a minimal agent example. For LLM-backed agents, configure your API keys and environment variables as recommended (see LLMConfig). Tools and group chat features may require additional setup.

    This section covers:
      - Basic installation (pip)
      - Installing optional dependencies for extended features
      - Post-installation verification
      - Environment variable setup for LLMs and toolkits

  examples:
    - title: "Basic Installation"
      description: "Install the core package using pip."
      code: |
        pip install autogen

    - title: "Installing with Optional Dependencies"
      description: |
        To use advanced features (e.g., group chat orchestration, interoperability with LangChain, or advanced toolkits), install the package with extras:
      code: |
        pip install autogen[group,langchain,toolkit]
        # or install all extras:
        pip install autogen[all]

    - title: "Verifying Installation"
      description: "Import the core abstractions and run a test agent."
      code: |
        python -c "from autogen import ConversableAgent; print('Install OK')"
        # Or, minimal agent test:
        from autogen import ConversableAgent
        agent = ConversableAgent(name="test_agent", system_message="Hello!", llm_config=None)
        print(agent.name)

    - title: "Setting Up LLM Provider Access"
      description: |
        Set environment variables (e.g., API keys) for your preferred LLM provider, then load them using LLMConfig.
      code: |
        export OPENAI_API_KEY="sk-..."
        # In Python:
        from autogen.llm_config import LLMConfig
        config = LLMConfig.from_json(env="OAI_CONFIG_LIST")
        agent = ConversableAgent("assistant", llm_config=config)

    - title: "Installing Development Version"
      description: |
        For the latest updates or to contribute, clone and install from source.
      code: |
        git clone https://github.com/microsoft/autogen.git
        cd autogen
        pip install -e ".[dev,all]"

  best_practices:
    - "Always use a virtual environment to isolate dependencies."
    - "Install only the extras you need to reduce dependency bloat."
    - "Verify installation with a minimal import or test agent."
    - "Set LLM API keys and config via environment variables, not hardcoded in scripts."
    - "Upgrade regularly to receive bug fixes and new features: pip install --upgrade autogen"
    - "Consult the official documentation for provider-specific setup (e.g., OpenAI, Azure, Gemini)."

  related_concepts:
    - name: "ConversableAgent (and Agent Protocols)"
      description: "After installation, this is the primary abstraction to instantiate and test, forming the basis for agentic communication."
    - name: "Tool and Toolkit"
      description: "Some tools may have extra dependencies; install relevant extras if you plan to use advanced toolkits or interoperability."
    - name: "LLMConfig"
      description: "Requires proper environment variable setup for API keys and model details; provider setup may affect installation."
    - name: "GroupChat and Group Patterns"
      description: "Group chat orchestration features are enabled via optional dependencies; install with the [group] extra."
    - name: "Tool Interoperability"
      description: "To use tools from other ecosystems (e.g., LangChain), ensure you install the relevant interoperability extras."
```