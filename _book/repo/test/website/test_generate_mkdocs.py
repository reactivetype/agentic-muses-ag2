# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
import tempfile
from pathlib import Path
from textwrap import dedent

import pytest

from autogen._website.generate_mkdocs import (
    absolute_to_relative,
    add_api_ref_to_mkdocs_template,
    add_authors_info_to_user_stories,
    add_excerpt_marker,
    add_notebooks_nav,
    filter_excluded_files,
    fix_asset_path,
    fix_internal_links,
    fix_internal_references,
    fix_snippet_imports,
    format_navigation,
    generate_community_insights_nav,
    generate_mkdocs_navigation,
    generate_url_slug,
    process_and_copy_files,
    process_blog_contents,
    process_blog_files,
    remove_mdx_code_blocks,
    transform_admonition_blocks,
    transform_card_grp_component,
    transform_tab_component,
)
from autogen._website.utils import NavigationGroup
from autogen.import_utils import optional_import_block, run_for_optional_imports

with optional_import_block():
    import jinja2

    assert jinja2


def test_exclude_files() -> None:
    files = [
        Path("/tmp/ag2/ag2/website/docs/user-guide/advanced-concepts/groupchat/groupchat.mdx"),
        Path("/tmp/ag2/ag2/website/docs/user-guide/advanced-concepts/groupchat/chat.txt"),
        Path("/tmp/ag2/ag2/website/docs/_blogs/2023-04-21-LLM-tuning-math/index.mdx"),
        Path("/tmp/ag2/ag2/website/docs/home/home.mdx"),
        Path("/tmp/ag2/ag2/website/docs/home/quick-start.mdx"),
    ]

    exclusion_list = ["docs/_blogs", "docs/home"]
    website_dir = Path("/tmp/ag2/ag2/website")

    actual = filter_excluded_files(files, exclusion_list, website_dir)
    expected = files[:2]
    assert actual == expected


def test_process_and_copy_files() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source directory structure
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()

        files = [
            src_dir / "user-guide" / "advanced-concepts" / "groupchat" / "groupchat.mdx",
            src_dir / "user-guide" / "advanced-concepts" / "groupchat" / "chat.txt",
            src_dir / "home" / "agent.png",
            src_dir / "home" / "quick-start.mdx",
            src_dir / "user-stories" / "2025-02-11-NOVA" / "index.mdx",
            src_dir / "user-stories" / "2023-02-11-HELLO-World" / "index.mdx",
        ]
        # Create the content for quick-start.mdx
        quick_start_content = dedent("""
            <Tip>
            It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.
            ```bash
            pip install -U autogen
            ```
            </Tip>

            <Warning>
            It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.
            </Warning>

            <Note>
            It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.
            </Note>

            <img src="https://github.com/AgentOps-AI/agentops/blob/main/docs/images/external/logo/banner-badge.png?raw=true" style={{ width: '40%' }} alt="AgentOps logo"/>

            """).lstrip()

        for file in files:
            file.parent.mkdir(parents=True, exist_ok=True)
            if file.name == "quick-start.mdx":
                file.write_text(quick_start_content)
            else:
                file.touch()

        mkdocs_output_dir = Path(tmpdir) / "mkdocs_output"
        mkdocs_output_dir.mkdir()

        process_and_copy_files(src_dir, mkdocs_output_dir, files)

        actual = list(filter(lambda x: x.is_file(), mkdocs_output_dir.rglob("*")))
        expected = [
            mkdocs_output_dir / "home" / "agent.png",
            mkdocs_output_dir / "home" / "quick-start.md",
            mkdocs_output_dir / "user-guide" / "advanced-concepts" / "groupchat" / "chat.txt",
            mkdocs_output_dir / "user-guide" / "advanced-concepts" / "groupchat" / "groupchat.md",
            mkdocs_output_dir / "user-stories" / "2025-02-11-NOVA" / "nova.md",
            mkdocs_output_dir / "user-stories" / "2023-02-11-HELLO-World" / "hello_world.md",
        ]
        assert len(actual) == len(expected)
        assert sorted(actual) == sorted(expected), f"{sorted(actual)} != {sorted(expected)}"

        # Assert the content of the transformed markdown file
        expected_quick_start_content = dedent("""
            !!! tip
                It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.
                ```bash
                pip install -U autogen
                ```

            !!! warning
                It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.

            !!! note
                It is important to never hard-code secrets into your code, therefore we read the OpenAI API key from an environment variable.

            <img src="https://github.com/AgentOps-AI/agentops/blob/main/docs/images/external/logo/banner-badge.png?raw=true" style={ width: '40%' } alt="AgentOps logo"/>

            """).lstrip()

        with open(mkdocs_output_dir / "home" / "quick-start.md") as f:
            actual_quick_start_content = f.read()

        assert actual_quick_start_content == expected_quick_start_content


def test_transform_tab_component() -> None:
    content = dedent("""This is a sample quick start page.
<Tabs>
    <Tab title="Chat with an agent">
```python
# 1. Import our agent class
from autogen import ConversableAgent

# 2. Define our LLM configuration for OpenAI's GPT-4o mini
#    uses the OPENAI_API_KEY environment variable
llm_config = {"api_type": "openai", "model": "gpt-4o-mini"}

# 3. Create our LLM agent
my_agent = ConversableAgent(
    name="helpful_agent",
    llm_config=llm_config,
    system_message="You are a poetic AI assistant, respond in rhyme.",
)

# 4. Run the agent with a prompt
chat_result = my_agent.run(message="In one sentence, what's the big deal about AI?")

# 5. Print the chat
print(chat_result.chat_history)
```
    </Tab>
    <Tab title="Two agent chat">
    example code
```python
llm_config = {"api_type": "openai", "model": "gpt-4o-mini"}
```


    </Tab>
</Tabs>

Some conclusion
""")

    expected = dedent("""This is a sample quick start page.
=== "Chat with an agent"
    ```python
    # 1. Import our agent class
    from autogen import ConversableAgent

    # 2. Define our LLM configuration for OpenAI's GPT-4o mini
    #    uses the OPENAI_API_KEY environment variable
    llm_config = {"api_type": "openai", "model": "gpt-4o-mini"}

    # 3. Create our LLM agent
    my_agent = ConversableAgent(
        name="helpful_agent",
        llm_config=llm_config,
        system_message="You are a poetic AI assistant, respond in rhyme.",
    )

    # 4. Run the agent with a prompt
    chat_result = my_agent.run(message="In one sentence, what's the big deal about AI?")

    # 5. Print the chat
    print(chat_result.chat_history)
    ```

=== "Two agent chat"
    example code
    ```python
    llm_config = {"api_type": "openai", "model": "gpt-4o-mini"}
    ```

Some conclusion
""")
    actual = transform_tab_component(content)
    assert actual == expected


def test_transform_card_grp_component() -> None:
    content = dedent("""This is a sample quick start page.
        <div class="popular-resources">
            <div class="card-group not-prose grid gap-x-4 sm:grid-cols-2">
                <CardGroup cols={2}>
                <Card>
                    <p>Hello World</p>
                </Card>
                <Card title="Quick Start" href="/docs/home/quick-start">
                    <p>Hello World</p>
                </Card>
                </CardGroup>
            </div>
        </div>
        """)

    expected = dedent("""This is a sample quick start page.
        <div class="popular-resources">
            <div class="card-group not-prose grid gap-x-4 sm:grid-cols-2">
                <div class="card">
                    <p>Hello World</p>
                </div>
                <a class="card" href="/docs/home/quick-start">
<h2>Quick Start</h2>
                    <p>Hello World</p>
                </a>
            </div>
        </div>
        """)
    actual = transform_card_grp_component(content)
    assert actual == expected


def test_fix_asset_path() -> None:
    content = dedent("""This is a sample quick start page.
<div class="key-feature">
    <img noZoom src="/static/img/conv_2.svg" alt="Multi-Agent Conversation Framework" />
    <a class="hero-btn" href="/docs/home/quick-start">
        <div>Getting Started - 3 Minute</div>
    </a>
</div>
![I -heart- AutoGen](/static/img/love.png)
""")
    expected = dedent("""This is a sample quick start page.
<div class="key-feature">
    <img noZoom src="/assets/img/conv_2.svg" alt="Multi-Agent Conversation Framework" />
    <a class="hero-btn" href="/docs/home/quick-start">
        <div>Getting Started - 3 Minute</div>
    </a>
</div>
![I -heart- AutoGen](/assets/img/love.png)
""")
    actual = fix_asset_path(content)
    assert actual == expected


def test_process_blog_files() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source directory structure

        mkdocs_dir = Path(tmpdir) / "mkdocs"
        mkdocs_dir.mkdir()

        src_dir = mkdocs_dir / "_blogs"
        src_dir.mkdir()

        # Create snippets directory
        snippets_dir = mkdocs_dir / "snippets"
        snippets_dir.mkdir()

        files = [
            src_dir / "2023-04-21-LLM-tuning-math" / "index.md",
            src_dir / "2023-04-21-LLM-tuning-math" / "cover.jpg",
            src_dir / "2023-04-21-LLM-tuning-math" / "cover.png",
            snippets_dir / "2023-04-21-LLM-tuning-math" / "index.md",
            snippets_dir / "2023-04-21-LLM-tuning-math" / "cover.jpg",
            snippets_dir / "2023-04-21-LLM-tuning-math" / "cover.png",
        ]

        # Create the files
        for file in files:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.touch()

        target_blog_dir = mkdocs_dir / "blog"

        authors_yml_path = mkdocs_dir / ".authors.yml"
        authors_yml_path.touch()

        # Assert the target_blog_dir should have posts directory and index.md file and .authors.yml file
        process_blog_files(mkdocs_dir, Path(authors_yml_path), snippets_dir)

        actual = list(filter(lambda x: x.is_file(), target_blog_dir.rglob("*")))
        expected = [
            target_blog_dir / "posts" / "2023-04-21-LLM-tuning-math" / "index.md",
            target_blog_dir / "posts" / "2023-04-21-LLM-tuning-math" / "cover.jpg",
            target_blog_dir / "posts" / "2023-04-21-LLM-tuning-math" / "cover.png",
            target_blog_dir / "index.md",
            target_blog_dir / ".authors.yml",
        ]
        assert len(actual) == len(expected)
        assert sorted(actual) == sorted(expected)

        target_snippet_dir = Path(tmpdir) / "snippets"
        assert target_snippet_dir.exists()
        assert len(list(filter(lambda x: x.is_file(), target_snippet_dir.rglob("*")))) == 3


def test_process_blog_contents() -> None:
    contents = dedent("""
    ---
    title: Does Model and Inference Parameter Matter in LLM Applications? - A Case Study for MATH
    authors: [sonichi]
    tags: [LLM, GPT, research]
    ---

    ![level 2 algebra](img/level2algebra.png)

    **TL;DR:**
    """)

    expected = "---" + dedent("""
    title: Does Model and Inference Parameter Matter in LLM Applications? - A Case Study for MATH
    authors: [sonichi]
    tags:
        - LLM
        - GPT
        - research
    categories:
        - LLM
        - GPT
        - research
    date: 2025-01-10
    slug: WebSockets
    ---

    ![level 2 algebra](img/level2algebra.png)

    **TL;DR:**

    <!-- more -->
    """)
    file = Path("tmp/ag2/ag2/website/mkdocs/docs/docs/_blogs/2025-01-10-WebSockets/index.md")
    actual = process_blog_contents(contents, file)
    assert actual == expected


def test_add_excerpt_marker() -> None:
    content = dedent("""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    We want to help you focus on building workflows and enhancing agents

    ### New agents need new tools

    some content

    """)
    expected = dedent("""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    We want to help you focus on building workflows and enhancing agents


    <!-- more -->

    ### New agents need new tools

    some content

    """)
    actual = add_excerpt_marker(content)
    assert actual == expected

    content = dedent("""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    We want to help you focus on building workflows and enhancing agents

    """)
    expected = dedent("""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    We want to help you focus on building workflows and enhancing agents

    <!-- more -->
    """)
    actual = add_excerpt_marker(content)
    assert actual == expected

    content = dedent(r"""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    \<!-- more -->

    We want to help you focus on building workflows and enhancing agents

    ### New agents need new tools

    some content

    """)
    expected = dedent("""
    ## Welcome DiscordAgent, SlackAgent, and TelegramAgent

    <!-- more -->

    We want to help you focus on building workflows and enhancing agents

    ### New agents need new tools

    some content

    """)
    actual = add_excerpt_marker(content)
    assert actual == expected


def test_fix_snippet_imports() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_snippets_dir = Path(tmpdir) / "snippets"

        # Create the directory structure
        reference_agents_dir = tmp_snippets_dir / "reference-agents"
        reference_agents_dir.mkdir(parents=True, exist_ok=True)

        # Create the MDX file with some sample content
        mdx_file_path = reference_agents_dir / "deep-research.mdx"
        mdx_file_content = dedent("""
        # Deep Research Component

        This is a deep research component that provides advanced capabilities.

        ## Features

        - Feature 1
        - Feature 2
        - Feature 3
        """)

        with open(mdx_file_path, "w") as f:
            f.write(mdx_file_content)

        content = dedent("""
        ## Introduction

        import DeepResearch from "/snippets/reference-agents/deep-research.mdx";

        <DeepResearch/>

        ## Conclusion
        """)
        expected = dedent("""
        ## Introduction


        # Deep Research Component

        This is a deep research component that provides advanced capabilities.

        ## Features

        - Feature 1
        - Feature 2
        - Feature 3


        <DeepResearch/>

        ## Conclusion
        """)

        actual = fix_snippet_imports(content, tmp_snippets_dir)
        assert actual == expected

        # Test case 2: Import from a directory outside the snippets directory
        content = dedent("""
        ## Introduction

        import DeepResearch from "/some-other-dir/reference-agents/deep-research.mdx";

        <DeepResearch/>

        ## Conclusion
        """)

        # In this case, the import should remain unchanged as we can't read from outside the snippets dir
        expected = dedent("""
        ## Introduction

        import DeepResearch from "/some-other-dir/reference-agents/deep-research.mdx";

        <DeepResearch/>

        ## Conclusion
        """)

        actual = fix_snippet_imports(content, tmp_snippets_dir)
        assert actual == expected


def test_generate_url_slug() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        blog_dir = Path(tmpdir) / "2025-02-13-DeepResearchAgent"
        blog_dir.mkdir(parents=True, exist_ok=True)

        tmpfile = blog_dir / "somefile.txt"
        tmpfile.touch()

        actual = generate_url_slug(tmpfile)
        expected = "\nslug: DeepResearchAgent"

        assert actual == expected


def test_add_notebooks_nav() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source directory structure
        metadata_yml_path = Path(tmpdir) / "notebooks_metadata.yml"

        # Add content
        metadata_yml_path.write_text(
            dedent("""
- title: "Run a standalone AssistantAgent"
  link: "/docs/use-cases/notebooks/notebooks/agentchat_assistant_agent_standalone"
  description: "Run a standalone AssistantAgent, browsing the web using the BrowserUseTool"
  image: ""
  tags:
    - "assistantagent"
    - "run"
    - "browser-use"
    - "webscraping"
    - "function calling"
  source: "/notebook/agentchat_assistant_agent_standalone.ipynb"

- title: "Mitigating Prompt hacking with JSON Mode in Autogen"
  link: "/docs/use-cases/notebooks/notebooks/JSON_mode_example"
  description: "Use JSON mode and Agent Descriptions to mitigate prompt manipulation and control speaker transition."
  image: ""
  tags:
    - "JSON"
    - "description"
    - "prompt hacking"
    - "group chat"
    - "orchestration"
  source: "/notebook/JSON_mode_example.ipynb"
""")
        )

        mkdocs_nav_path = Path(tmpdir) / "navigation_template.txt"

        mkdocs_nav_path.write_text(
            dedent("""
- Use Cases
    - Use cases
        - [Customer Service](docs/use-cases/use-cases/customer-service.md)
        - [Game Design](docs/use-cases/use-cases/game-design.md)
        - [Travel Planning](docs/use-cases/use-cases/travel-planning.md)
    - Notebooks
        - [All Notebooks](docs/use-cases/notebooks/Notebooks.md)
    - [Community Gallery](docs/use-cases/community-gallery/community-gallery.md)
- API References
{api}
""")
        )

        add_notebooks_nav(mkdocs_nav_path, metadata_yml_path)

        expected = dedent("""
- Use Cases
    - Use cases
        - [Customer Service](docs/use-cases/use-cases/customer-service.md)
        - [Game Design](docs/use-cases/use-cases/game-design.md)
        - [Travel Planning](docs/use-cases/use-cases/travel-planning.md)
    - Notebooks
        - [All Notebooks](docs/use-cases/notebooks/Notebooks.md)
        - [Run a standalone AssistantAgent](docs/use-cases/notebooks/notebooks/agentchat_assistant_agent_standalone)
        - [Mitigating Prompt hacking with JSON Mode in Autogen](docs/use-cases/notebooks/notebooks/JSON_mode_example)
    - [Community Gallery](docs/use-cases/community-gallery/community-gallery.md)
- API References
{api}
""")

        actual = mkdocs_nav_path.read_text()
        assert actual == expected


def test_generate_user_stories_nav() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create User Stories directory
        user_stories_dir = Path(tmpdir) / "docs" / "user-stories"
        community_talks_dir = Path(tmpdir) / "docs" / "community-talks"

        file_1 = user_stories_dir / "2025-03-11-NOVA" / "nova.md"
        file_1.parent.mkdir(parents=True, exist_ok=True)
        file_1.write_text("""---
title: Unlocking the Power of Agentic Workflows at Nexla with AG2
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

> AG2 has been instrumental in helping Nexla build NOVA,
""")

        file_2 = user_stories_dir / "2025-02-11-NOVA" / "nova.md"
        file_2.parent.mkdir(parents=True, exist_ok=True)
        file_2.write_text("""---
title: Some other text
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

> AG2 has been instrumental in helping Nexla build NOVA,
""")

        file_3 = community_talks_dir / "2025-02-11-NOVA" / "nova.md"
        file_3.parent.mkdir(parents=True, exist_ok=True)
        file_3.write_text("""---
title: Some other text
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

> AG2 has been instrumental in helping Nexla build NOVA,
""")

        # Create source directory structure
        mkdocs_nav_path = Path(tmpdir) / "navigation_template.txt"

        mkdocs_nav_path.write_text(
            dedent("""
- Use Cases
    - Use cases
        - [Customer Service](docs/use-cases/use-cases/customer-service.md)
        - [Game Design](docs/use-cases/use-cases/game-design.md)
        - [Travel Planning](docs/use-cases/use-cases/travel-planning.md)
    - Notebooks
        - [Notebooks](docs/use-cases/notebooks/Notebooks.md)
    - [Community Gallery](docs/use-cases/community-gallery/community-gallery.md)
- Blog
    - [Contributing](docs/contributor-guide/contributing.md)
    - [Setup Development Environment](docs/contributor-guide/setup-development-environment.md)
""")
        )

        generate_community_insights_nav(Path(tmpdir), mkdocs_nav_path)

        expected = dedent("""
- Use Cases
    - Use cases
        - [Customer Service](docs/use-cases/use-cases/customer-service.md)
        - [Game Design](docs/use-cases/use-cases/game-design.md)
        - [Travel Planning](docs/use-cases/use-cases/travel-planning.md)
    - Notebooks
        - [Notebooks](docs/use-cases/notebooks/Notebooks.md)
    - [Community Gallery](docs/use-cases/community-gallery/community-gallery.md)
- Community Insights
    - User Stories
        - [Unlocking the Power of Agentic Workflows at Nexla with AG2](docs/user-stories/2025-03-11-NOVA/nova.md)
        - [Some other text](docs/user-stories/2025-02-11-NOVA/nova.md)
    - Community Talks
        - [Some other text](docs/community-talks/2025-02-11-NOVA/nova.md)
- Blog
    - [Contributing](docs/contributor-guide/contributing.md)
    - [Setup Development Environment](docs/contributor-guide/setup-development-environment.md)
""")

        actual = mkdocs_nav_path.read_text()
        assert actual == expected


def test_add_authors_info_to_user_stories() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create User Stories directory
        mkdocs_output_dir = Path(tmpdir) / "mkdocs" / "docs" / "docs"
        user_stories_dir = mkdocs_output_dir / "user-stories"

        file_1 = user_stories_dir / "2025-03-11-NOVA" / "index.md"
        file_1.parent.mkdir(parents=True, exist_ok=True)
        file_1.write_text("""---
title: Unlocking the Power of Agentic Workflows at Nexla with AG2
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

> AG2 has been instrumental in helping Nexla build NOVA,
""")

        file_2 = user_stories_dir / "2025-02-11-NOVA" / "index.md"
        file_2.parent.mkdir(parents=True, exist_ok=True)
        file_2.write_text("""---
title: Some other text
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

> AG2 has been instrumental in helping Nexla build NOVA,
""")

        authors_yml = Path(tmpdir) / "blogs_and_user_stories_authors.yml"

        authors_yml.write_text("""
authors:
  sonichi:
    name: Chi Wang
    description: Founder of AutoGen (now AG2) & FLAML
    url: https://www.linkedin.com/in/chi-wang-autogen/
    avatar: https://github.com/sonichi.png

  qingyunwu:
    name: Qingyun Wu
    description: Co-Founder of AutoGen/AG2 & FLAML, Assistant Professor at Penn State University
    url: https://qingyun-wu.github.io/
    avatar: https://github.com/qingyun-wu.png
""")

        add_authors_info_to_user_stories(Path(tmpdir))

        actual = file_1.read_text()
        expected = dedent("""---
title: Unlocking the Power of Agentic Workflows at Nexla with AG2
authors:
  - sonichi
  - qingyunwu
tags: [data automation, agents, AG2, Nexla]
---

<div class="blog-authors">
<p class="authors">Authors:</p>
<div class="card-group">

<div class="card">
    <div class="col card">
      <div class="img-placeholder">
        <img noZoom src="https://github.com/sonichi.png" />
      </div>
      <div>
        <p class="name">Chi Wang</p>
        <p>Founder of AutoGen (now AG2) & FLAML</p>
      </div>
    </div>
</div>

<div class="card">
    <div class="col card">
      <div class="img-placeholder">
        <img noZoom src="https://github.com/qingyun-wu.png" />
      </div>
      <div>
        <p class="name">Qingyun Wu</p>
        <p>Co-Founder of AutoGen/AG2 & FLAML, Assistant Professor at Penn State University</p>
      </div>
    </div>
</div>

</div>
</div>

> AG2 has been instrumental in helping Nexla build NOVA,
""")
        assert actual == expected


class TestRemoveMdxCodeBlocks:
    def test_simple_example(self) -> None:
        """Test with the example provided in the requirements."""
        input_content = """````mdx-code-block
!!! info "Requirements"
    Some extra dependencies are needed for this notebook, which can be installed via pip:

    ```bash
    pip install ag2[openai,lmm]
    ```

    For more information, please refer to the [installation guide](/docs/user-guide/basic-concepts/installing-ag2).
````"""

        expected_output = """!!! info "Requirements"
    Some extra dependencies are needed for this notebook, which can be installed via pip:

    ```bash
    pip install ag2[openai,lmm]
    ```

    For more information, please refer to the [installation guide](/docs/user-guide/basic-concepts/installing-ag2)."""

        assert remove_mdx_code_blocks(input_content) == expected_output

    def test_multiple_blocks(self) -> None:
        """Test with multiple mdx-code-blocks in the content."""
        input_content = """Some text before

````mdx-code-block
!!! note
    This is a note
````

Some text in between

````mdx-code-block
!!! warning
    This is a warning
````

Some text after"""

        expected_output = """Some text before

!!! note
    This is a note

Some text in between

!!! warning
    This is a warning

Some text after"""

        assert remove_mdx_code_blocks(input_content) == expected_output

    def test_no_mdx_blocks(self) -> None:
        """Test with content that doesn't have any mdx-code-blocks."""
        input_content = """# Regular Markdown

This is some regular markdown content.

```python
def regular_code():
    return "not inside mdx-code-block"
```"""

        assert remove_mdx_code_blocks(input_content) == input_content


class TestTransformAdmonitionBlocks:
    def test_basic_admonition(self) -> None:
        """Test basic admonition block without a title."""
        content = """
Some text before

:::note
This is a simple note.
:::

Some text after
"""
        expected = """
Some text before

!!! note
    This is a simple note.

Some text after
"""
        actual = transform_admonition_blocks(content)
        assert actual == expected

    def test_admonition_with_title(self) -> None:
        """Test admonition block with a title."""
        content = """
:::warning Important Alert
This is a warning with a title.
:::
"""
        expected = """
!!! warning "Important Alert"
    This is a warning with a title.
"""
        actual = transform_admonition_blocks(content)
        assert actual == expected

    def test_multiple_admonitions(self) -> None:
        """Test multiple admonition blocks in the same content."""
        content = """
:::tip
Tip content
:::

Some text in between

:::danger Caution
Danger content
:::
"""
        expected = """
!!! tip
    Tip content

Some text in between

!!! danger "Caution"
    Danger content
"""
        actual = transform_admonition_blocks(content)
        assert actual == expected

    def test_admonition_with_multiline_content(self) -> None:
        """Test admonition with multiple lines of content."""
        content = """
:::note
Line 1
Line 2
Line 3
:::
"""
        expected = """
!!! note
    Line 1
    Line 2
    Line 3
"""
        assert transform_admonition_blocks(content) == expected

    def test_admonition_with_indented_content(self) -> None:
        """Test admonition with indented content."""
        content = """
:::note
    This line is indented.
        This line is more indented.
    Back to first level.
:::
"""
        expected = """
!!! note
    This line is indented.
        This line is more indented.
    Back to first level.
"""
        assert transform_admonition_blocks(content) == expected

    def test_admonition_with_code_block(self) -> None:
        """Test admonition containing a code block."""
        content = """
:::tip Code Example
Here's some code:

```python
def hello():
    print("Hello world")
```
:::
"""
        expected = """
!!! tip "Code Example"
    Here's some code:

    ```python
    def hello():
        print("Hello world")
    ```
"""
        actual = transform_admonition_blocks(content)
        assert actual == expected

    def test_admonition_with_lists(self) -> None:
        """Test admonition containing lists."""
        content = """
:::note
- Item 1
- Item 2
  - Nested item
- Item 3
:::
"""
        expected = """
!!! note
    - Item 1
    - Item 2
      - Nested item
    - Item 3
"""
        assert transform_admonition_blocks(content) == expected

    def test_admonition_with_blockquotes(self) -> None:
        """Test admonition containing blockquotes."""
        content = """
:::info
Here's a quote:

> This is a blockquote
> Multiple lines
:::
"""
        expected = """
!!! info
    Here's a quote:

    > This is a blockquote
    > Multiple lines
"""
        actual = transform_admonition_blocks(content)
        assert actual == expected

    def test_admonition_type_mapping(self) -> None:
        """Test mapping of admonition types."""
        content = """
:::Tip
This should map to lowercase 'tip'
:::

:::warning
This should stay as 'warning'
:::

:::custom
This should stay as 'custom'
:::
"""
        expected = """
!!! tip
    This should map to lowercase 'tip'

!!! warning
    This should stay as 'warning'

!!! custom
    This should stay as 'custom'
"""
        assert transform_admonition_blocks(content) == expected

    def test_invalid_syntax_admonition(self) -> None:
        """Test that original content is preserved for malformed admonition syntax."""
        content = """
    Some text before

    :::
    This is missing a type specifier
    :::

    Some text after
    """
        # The output should be identical to the input
        assert transform_admonition_blocks(content) == content


@pytest.fixture
def navigation() -> list[NavigationGroup]:
    return [
        {"group": "Quick Start", "pages": ["docs/quick-start"]},
        {
            "group": "User Guide",
            "pages": [
                {
                    "group": "Basic Concepts",
                    "pages": [
                        "docs/user-guide/basic-concepts/installing-ag2",
                        {
                            "group": "LLM Configuration",
                            "pages": [
                                "docs/user-guide/basic-concepts/llm-configuration/llm-configuration",
                                "docs/user-guide/basic-concepts/llm-configuration/structured-outputs",
                            ],
                        },
                        "docs/user-guide/basic-concepts/conversable-agent",
                        "docs/user-guide/basic-concepts/human-in-the-loop",
                        {
                            "group": "Orchestrating Agents",
                            "pages": [
                                "docs/user-guide/basic-concepts/orchestration/orchestrations",
                                "docs/user-guide/basic-concepts/orchestration/sequential-chat",
                            ],
                        },
                    ],
                },
                {"group": "Advanced Concepts", "pages": ["docs/user-guide/advanced-concepts/rag"]},
            ],
        },
        {
            "group": "Contributor Guide",
            "pages": [
                "docs/contributing/contributing",
            ],
        },
    ]


@pytest.fixture
def expected_nav() -> str:
    return """- [Quick Start](docs/quick-start.md)
- User Guide
    - [Basic Concepts](docs/user-guide/basic-concepts/overview.md)
        - [Installing AG2](docs/user-guide/basic-concepts/installing-ag2.md)
        - LLM Configuration
            - [LLM Configuration](docs/user-guide/basic-concepts/llm-configuration/llm-configuration.md)
            - [Structured Outputs](docs/user-guide/basic-concepts/llm-configuration/structured-outputs.md)
        - [Conversable Agent](docs/user-guide/basic-concepts/conversable-agent.md)
        - [Human In The Loop](docs/user-guide/basic-concepts/human-in-the-loop.md)
        - Orchestrating Agents
            - [Orchestrations](docs/user-guide/basic-concepts/orchestration/orchestrations.md)
            - [Sequential Chat](docs/user-guide/basic-concepts/orchestration/sequential-chat.md)
    - Advanced Concepts
        - [RAG](docs/user-guide/advanced-concepts/rag.md)
- Contributor Guide
    - [Contributing](docs/contributing/contributing.md)"""


def test_format_navigation(navigation: list[NavigationGroup], expected_nav: str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        actual = format_navigation(navigation, Path(tmpdir))
        assert actual == expected_nav


def test_add_api_ref_to_mkdocs_template() -> None:
    mkdocs_nav = """- Home
    - [Home](docs/home/home.md)
- User Guide
    - Basic Concepts
        - [Installing AG2](docs/user-guide/basic-concepts/installing-ag2.md)
        - LLM Configuration
            - [LLM Configuration](docs/user-guide/basic-concepts/llm-configuration/llm-configuration.md)
        - [Websurferagent](docs/user-guide/reference-agents/websurferagent.md)
- Contributor Guide
    - [Contributing](docs/contributor-guide/contributing.md)
"""

    expected = """- Home
    - [Home](docs/home/home.md)
- User Guide
    - Basic Concepts
        - [Installing AG2](docs/user-guide/basic-concepts/installing-ag2.md)
        - LLM Configuration
            - [LLM Configuration](docs/user-guide/basic-concepts/llm-configuration/llm-configuration.md)
        - [Websurferagent](docs/user-guide/reference-agents/websurferagent.md)
- API References
{api}
- Contributor Guide
    - [Contributing](docs/contributor-guide/contributing.md)
"""
    section_to_follow = "Contributor Guide"
    actual = add_api_ref_to_mkdocs_template(mkdocs_nav, section_to_follow)
    assert actual == expected


@run_for_optional_imports(["jinja2"], "docs")
def test_generate_mkdocs_navigation(navigation: list[NavigationGroup], expected_nav: str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source directory structure
        website_dir = Path(tmpdir) / "website_root"
        website_dir.mkdir()

        # Create mkdocs directory
        mkdocs_root_dir = Path(tmpdir) / "mkdocs_root"
        mkdocs_root_dir.mkdir()

        mintlify_nav_template_path = website_dir / "mint-json-template.json.jinja"
        mkdocs_nav_path = mkdocs_root_dir / "docs" / "navigation_template.txt"
        mkdocs_nav_path.parent.mkdir(parents=True, exist_ok=True)
        mkdocs_nav_path.touch()

        summary_md_path = mkdocs_root_dir / "docs" / "SUMMARY.md"

        mintlify_nav_content = (
            """
        {
  "$schema": "https://mintlify.com/schema.json",
  "name": "AG2",
    "navigation": """
            + json.dumps(navigation)
            + """ }"""
        )

        mintlify_nav_template_path.write_text(mintlify_nav_content)

        nav_exclusions = ["Contributor Guide"]
        generate_mkdocs_navigation(website_dir, mkdocs_root_dir, nav_exclusions)
        actual = mkdocs_nav_path.read_text()
        expected = (
            """---
search:
  exclude: true
---
"""
            + expected_nav.replace(
                """
- Contributor Guide
    - [Contributing](docs/contributing/contributing.md)""",
                "",
            )
            + "\n- Blog\n    - [Blog](docs/blog/index.md)"
            + "\n"
        )

        assert actual == expected
        assert summary_md_path.read_text() == expected


def test_fix_internal_references() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create source directory structure
        tmpdir_path = Path(tmpdir)
        mkdocs_dir = tmpdir_path / "mkdocs"
        mkdocs_dir.mkdir()

        # Create the files
        file = mkdocs_dir / "quick-start.md"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

        actual = fix_internal_references("/mkdocs/quick-start.md", tmpdir_path)
        expected = "/mkdocs/quick-start.md"

        assert actual == expected

        notebooks_dir = tmpdir_path / "notebooks"
        notebooks_dir.mkdir()

        # Create the files
        file = notebooks_dir / "quick-start.md"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

        # Create the files
        file = tmpdir_path / "Notebooks.md"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

        actual = fix_internal_references("/Notebooks", tmpdir_path)
        expected = "/Notebooks"

        assert actual == expected

        actual = fix_internal_references("/mkdocs", tmpdir_path)
        expected = "/mkdocs/quick-start"

        assert actual == expected

        actual = fix_internal_references("/docs/api-reference", tmpdir_path)
        expected = "/docs/api-reference/autogen/AfterWork"

        assert actual == expected

        actual = fix_internal_references("/docs/api-reference/autogen/ConversableAgent#initiate-all-chats", tmpdir_path)
        expected = "/docs/api-reference/autogen/ConversableAgent#autogen.ConversableAgent.initiate_all_chats"

        assert actual == expected


class TestFixInternalLinks:
    def test_absolute_to_relative(self) -> None:
        source_path = os.path.join("docs", "home", "quick-start.md")
        content = os.path.join("docs", "user-guide", "basic-concepts", "installing-ag2")

        expected = os.path.join("..", "..", "user-guide", "basic-concepts", "installing-ag2")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "blog", "2025-02-05-Communication-Agents")
        content = os.path.join("docs", "api-reference", "autogen", "UserProxyAgent")

        expected = os.path.join("..", "..", "..", "..", "..", "api-reference", "autogen", "UserProxyAgent")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "user-guide", "basic-concepts", "tools", "index.md")
        content = os.path.join("docs", "user-guide", "basic-concepts", "tools", "interop", "langchain")

        expected = os.path.join(".", "interop", "langchain")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "user-guide", "basic-concepts", "tools", "index.md")
        content = os.path.join("docs", "user-guide", "basic-concepts", "tools", "basics")

        expected = os.path.join(".", "basics")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "home", "home.md")
        content = os.path.join("docs", "home", "quick-start")

        expected = os.path.join("..", "quick-start")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "contributor-guide", "how-ag2-works", "hooks.md")
        content = os.path.join("docs", "contributor-guide", "how-ag2-works", "initiate-chat")

        expected = os.path.join("..", "initiate-chat")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

        source_path = os.path.join("docs", "user-guide", "reference-tools", "index.md")
        content = os.path.join("docs", "api-reference", "autogen", "tools", "experimental", "GoogleSearchTool")

        expected = os.path.join("..", "..", "api-reference", "autogen", "tools", "experimental", "GoogleSearchTool")
        actual = absolute_to_relative(source_path, content)

        assert actual == expected

    def test_fix_internal_links(self) -> None:
        source_path = "/docs/home/quick-start.md"
        content = dedent("""AG2 (formerly AutoGen) is an open-source programming framework for building AI agents
!!! tip
    Learn more about configuring LLMs for agents
        [here](/docs/user-guide/basic-concepts/llm-configuration.md).

### Where to Go Next?

- [Sample Link](/docs/home/slow-start.md)
- Go through the [basic concepts](/docs/user-guide/basic-concepts/installing-ag2) to get started
- Once you're ready, hit the [advanced concepts](/docs/user-guide/advanced-concepts/rag)
- Explore the [API Reference](/docs/api-reference/autogen/overview)
- Chat on [Discord](https://discord.gg/pAbnFJrkgZ)
- Follow on [X](https://x.com/ag2oss)

If you like our project, please give it a [star](https://github.com/ag2ai/ag2) on GitHub. If you are interested in contributing, please read [Contributor's Guide](/docs/contributor-guide/contributing).

<img alt="DeepResearchAgent workflow" src="/snippets/reference-agents/img/DeepResearchAgent.png">

![DeepResearchAgent workflow](/snippets/reference-agents/img/DeepResearchAgent.png)

<img class="hero-logo" noZoom src="/assets/img/ag2.svg" alt="AG2 Logo" />

[Cross-Framework LLM Tool Integration](/docs/blog/2024-12-20-Tools-interoperability)

""")
        expected = dedent(
            """AG2 (formerly AutoGen) is an open-source programming framework for building AI agents
!!! tip
    Learn more about configuring LLMs for agents
        [here]({}).

### Where to Go Next?

- [Sample Link]({})
- Go through the [basic concepts]({}) to get started
- Once you're ready, hit the [advanced concepts]({})
- Explore the [API Reference]({})
- Chat on [Discord](https://discord.gg/pAbnFJrkgZ)
- Follow on [X](https://x.com/ag2oss)

If you like our project, please give it a [star](https://github.com/ag2ai/ag2) on GitHub. If you are interested in contributing, please read [Contributor's Guide]({}).

<img alt="DeepResearchAgent workflow" src="{}">

![DeepResearchAgent workflow]({})

<img class="hero-logo" noZoom src="{}" alt="AG2 Logo" />

[Cross-Framework LLM Tool Integration]({})

""".format(
                os.path.join("..", "..", "user-guide", "basic-concepts", "llm-configuration.md"),
                os.path.join("..", "slow-start.md"),
                os.path.join("..", "..", "user-guide", "basic-concepts", "installing-ag2"),
                os.path.join("..", "..", "user-guide", "advanced-concepts", "rag"),
                os.path.join("..", "..", "api-reference", "autogen", "overview"),
                os.path.join("..", "..", "contributor-guide", "contributing"),
                os.path.join("..", "..", "..", "snippets", "reference-agents", "img", "DeepResearchAgent.png"),
                os.path.join("..", "..", "..", "snippets", "reference-agents", "img", "DeepResearchAgent.png"),
                os.path.join("..", "..", "..", "assets", "img", "ag2.svg"),
                os.path.join("..", "..", "blog", "2024", "12", "20", "Tools-interoperability"),
            )
        )
        actual = fix_internal_links(source_path, content)
        assert actual == expected
