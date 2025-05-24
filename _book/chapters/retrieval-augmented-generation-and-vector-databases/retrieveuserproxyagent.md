# RetrieveUserProxyAgent

## Overview

The **RetrieveUserProxyAgent** is a specialized agent pattern used in Retrieval Augmented Generation (RAG) systems, enabling intelligent search and retrieval of relevant information from large document collections or knowledge bases. By interfacing with vector databases, the agent can efficiently fetch contextually similar documents or chunks, which are then used to augment generative models (like LLMs) for more accurate, grounded responses. RetrieveUserProxyAgent acts as an orchestrator that manages user queries, interacts with retrieval tools (e.g., vector search APIs), and applies logic for context-informed generation.

---

## Explanation

The RetrieveUserProxyAgent sits at the core of a RAG pipeline, bridging user input with backend retrieval and generation functionality. Its main responsibilities include:

1. **Processing User Queries**: Accepts natural language queries and applies necessary pre-processing, such as chunking or tokenization.
2. **Interfacing with Vector Databases**: Converts queries into vector embeddings and searches against vector databases (e.g., Pinecone, FAISS, ChromaDB) for semantically similar documents or passages.
3. **Contextual Retrieval**: Uses conditional logic and context variables to refine retrieval results, ensuring relevance to the user's intent.
4. **Augmenting Generation**: Supplies retrieved content as context to a generative model (e.g., GPT-4), enabling grounded and contextualized responses.
5. **Tool and Function Interoperability**: Orchestrates and integrates multiple tools—embedding models, vector stores, and LLMs—often by invoking specific functions or APIs.

### Example Flow

1. **User Query**: "What were the main findings of the 2023 climate report?"
2. **Embedding & Vector Search**: Query embedded and matched against document chunks in the vector DB.
3. **Retrieval**: Top-k relevant passages retrieved.
4. **Context Assembly**: Chosen passages assembled as additional context.
5. **Generation**: LLM generates a response using both user query and retrieved context.

### Chunking and Tokenization

Efficient retrieval often requires documents to be split (chunked) into overlapping or non-overlapping segments, ensuring that each chunk fits within model or database token limitations while preserving context. Tokenization strategies are chosen to balance retrieval granularity and performance.

---

## Examples

### Example 1: Simple RetrieveUserProxyAgent Workflow (Python Pseudocode)

```python
from my_agent_framework import RetrieveUserProxyAgent
from my_vector_db import VectorStore
from my_embedding_model import EmbeddingModel
from my_llm import LLM

# Initialize components
embedding_model = EmbeddingModel()
vector_store = VectorStore(index_name="knowledge_base")
llm = LLM(model_name="gpt-4")

# Define the agent
agent = RetrieveUserProxyAgent(
    embedding_model=embedding_model,
    vector_store=vector_store,
    llm=llm,
    chunk_size=512,  # tokens per chunk
    overlap=64,      # token overlap
)

# User query
query = "Summarize the key findings from the 2023 climate report."

# Agent processes the query
response = agent.generate(query)

print(response)
```

### Example 2: Custom Chunking and Conditional Logic

```python
def custom_chunk(document, max_tokens=512, overlap=64):
    # Your custom chunking logic
    # Returns a list of text chunks
    pass

agent = RetrieveUserProxyAgent(
    ...,
    chunker=custom_chunk,
    retrieval_filter=lambda chunk, query: "climate" in chunk.lower() or "2023" in chunk,
)
```

### Example 3: Tool Interoperability

```python
# Using different vector backends
vector_store = PineconeVectorStore(api_key="...")
agent = RetrieveUserProxyAgent(vector_store=vector_store, ...)

# Using a different embedding model
embedding_model = OpenAIEmbeddingModel(api_key="...")
agent.embedding_model = embedding_model
```

---

## Best Practices

- **Chunk Size Tuning**: Optimize chunk size and overlap to balance recall and precision; too small loses context, too large may miss details.
- **Tokenization Consistency**: Ensure the same tokenization method is used during both document indexing and query time.
- **Backend Flexibility**: Design agents to easily switch between vector backends (e.g., FAISS, Pinecone, ChromaDB) as requirements evolve.
- **Context Window Awareness**: Be mindful of model input size limits when assembling retrieved context for the generative model.
- **Conditional Retrieval**: Use context variables and custom filters to fine-tune which chunks are considered relevant.
- **Evaluate Retrieval Quality**: Regularly benchmark retrieval results and tune scoring thresholds.

**Common Pitfalls:**
- Indexing and querying with different embedding models or tokenization schemes.
- Ignoring context window limits, leading to truncated or incomplete prompts.
- Over-reliance on retrieval without validating factuality in generation.

---

## Related Concepts

- [Retrieval Augmented Generation (RAG)](https://huggingface.co/docs/transformers/main/en/tasks/rag)
- [Vector Databases (e.g., Pinecone, FAISS, ChromaDB)](https://www.pinecone.io/learn/vector-database/)
- [Chunking and Tokenization Strategies](https://docs.langchain.com/docs/modules/data_connection/text_embedding/chunking/)
- [Tool/Function Interoperability](./tool_function_interoperability.md)
- [Context Variables and Conditional Logic](./context_variables_conditional_logic.md)
- [Prompt Engineering for RAG](https://www.promptingguide.ai/techniques/contextual-prompting)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)

For further reading, see:
- [LangChain: Retrieval-Augmented Generation](https://python.langchain.com/docs/use_cases/question_answering/)
- [Haystack: Building RAG Pipelines](https://haystack.deepset.ai/tutorials/rag)

---