```yaml
content:
  overview: |
    Retrieval Augmented Generation (RAG) is an advanced technique that combines Large Language Models (LLMs) with external information retrieval systems to enhance accuracy, reduce hallucination, and enable up-to-date or domain-specific responses. In an agentic AI framework, RAG is implemented by integrating agents with vector databases and document agents, enabling dynamic search, retrieval, and synthesis of relevant information during conversations.

  explanation: |
    Traditional LLMs generate responses solely based on their trained knowledge, which may be outdated or incomplete. Retrieval Augmented Generation (RAG) addresses this limitation by allowing LLMs to access and incorporate information retrieved from external sources—such as indexed documents, knowledge bases, or vector databases—at generation time.

    In agent-based frameworks, RAG is achieved by:
      - Registering retrieval tools (functions that query vector databases or search corpora) with ConversableAgent or specialized document agents.
      - Using these tools within the LLM's function-calling interface, so the model can proactively fetch and ground its answers on real data.
      - Employing multi-agent patterns, where one agent specializes in retrieval (DocumentAgent), another in synthesis, and orchestration is managed via GroupChat or GroupChatManager.

    Vector database integrations (e.g., with FAISS, Pinecone, Chroma, Weaviate) are central to RAG, as they enable fast, semantic similarity search over large collections of text or documents. Tools encapsulate these retrieval operations and expose them to the agent layer. Document agents are preconfigured ConversableAgent subclasses or wrappers designed to handle document ingestion, embedding, and retrieval workflows, abstracting the low-level vector store logic.

    RAG workflows typically involve:
      1. User query: An agent receives a question.
      2. Retrieval: The agent uses a registered retrieval tool to search the vector DB for relevant passages.
      3. Synthesis: The agent (or a dedicated synthesizer agent) combines the retrieved snippets with LLM reasoning to produce a grounded response.

    This modular approach allows for flexible, updatable, and auditable agentic systems capable of leveraging both LLM reasoning and external knowledge.

  examples:
    - title: "Basic RAG with ConversableAgent and Vector DB"
      description: "Using a retrieval tool that queries a vector database, registered with a ConversableAgent."
      code: |
        from autogen import ConversableAgent
        from autogen.tools import tool

        # Assume you have a vector DB client (e.g., FAISS, Chroma)
        vector_db = ...  # Initialized vector DB client

        @tool(name="retrieve_docs", description="Retrieve relevant documents from the vector DB")
        def retrieve_docs(query: str, top_k: int = 3):
            # Returns the top_k most similar documents
            return vector_db.search(query, top_k=top_k)

        agent = ConversableAgent(
            name="rag_agent",
            system_message="You are a helpful AI assistant with access to a document database.",
            llm_config={...}
        )
        agent.register_tool(retrieve_docs)

        # Now, when the agent is prompted, LLM can choose to call retrieve_docs
        response = agent.initiate_chat(
            user_proxy,
            message="What does the latest company policy say about remote work?"
        )

    - title: "DocumentAgent for End-to-End RAG"
      description: "Using a specialized DocumentAgent to manage document ingestion, embedding, and retrieval."
      code: |
        from autogen.agentchat.document_agent import DocumentAgent

        doc_agent = DocumentAgent(
            name="doc_agent",
            vector_db_config={
                "provider": "chroma",
                "persist_dir": "./db",
                # Other DB-specific config
            },
            llm_config={...}
        )

        # Add documents to the agent's vector DB
        doc_agent.ingest_documents([
            {"title": "Policy", "content": "Remote work is allowed up to 3 days per week ..."},
            # more documents
        ])

        # User query triggers retrieval and synthesis
        answer = doc_agent.initiate_chat(
            user_proxy,
            message="What are the company’s remote work rules?"
        )

    - title: "Group Pattern: Retrieval and Synthesis Agents"
      description: "Orchestrating a pipeline where one agent retrieves, and another synthesizes the final answer."
      code: |
        from autogen import GroupChat, GroupChatManager, ConversableAgent
        from autogen.agentchat.document_agent import DocumentAgent
        from autogen.agentchat.group.patterns.auto import AutoPattern

        retriever = DocumentAgent(name="retriever", vector_db_config={...}, llm_config={...})
        synthesizer = ConversableAgent(name="synthesizer", system_message="Summarize the retrieved docs.", llm_config={...})

        agents = [retriever, synthesizer]
        pattern = AutoPattern(initial_agent=retriever, agents=agents)
        groupchat, manager = pattern.prepare_group_chat(max_rounds=3, messages=[{"content": "Find info on remote work policy."}])

        # Start the chat
        retriever.initiate_chat(manager, message="User asked: What is the remote work policy?")

  best_practices:
    - "Always provide clear tool descriptions and parameter schemas to ensure LLMs call retrieval tools correctly."
    - "Preprocess and chunk documents appropriately for optimal retrieval quality—avoid excessively large or small chunks."
    - "Test retrieval accuracy and tune embedding/model configs for your domain."
    - "Monitor and log retrieval results to audit LLM responses and ensure proper grounding."
    - "Keep retrieval and synthesis steps modular—use group patterns for complex workflows."
    - "Manage vector DB storage and memory to avoid bloat, especially in multi-user or multi-session settings."
    - "Use dedicated document agents for scalable or production RAG systems."

  related_concepts:
    - name: "Tool and Toolkit"
      description: "Retrieval functions are registered as tools, enabling LLM function-calling for RAG. Use toolkits to manage multiple retrieval and synthesis utilities."
    - name: "ConversableAgent"
      description: "The core abstraction that supports tool registration and interaction, serving as the backbone for RAG-capable agents."
    - name: "DocumentAgent"
      description: "A specialized agent for RAG, abstracting vector store management, retrieval, and ingestion."
    - name: "GroupChat and Group Patterns"
      description: "Enable multi-agent RAG workflows, separating retrieval and synthesis for more modular designs."
    - name: "LLMConfig"
      description: "Standardizes model configuration for both retrieval and synthesis agents, ensuring consistent API usage and context management."
    - name: "Tool Interoperability"
      description: "Allows integration of retrieval tools from other ecosystems (e.g., LangChain) into the agent framework for RAG."
```