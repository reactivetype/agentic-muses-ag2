# Querying and chunking strategies

## Overview

Retrieval Augmented Generation (RAG) combines traditional information retrieval with generative AI by leveraging vector databases to store and search over embeddings of documents or knowledge sources. Two critical components for effective RAG systems are **querying** (how user questions are transformed and matched against the database) and **chunking** (how documents are split into retrievable units). Optimal strategies for querying and chunking significantly impact search accuracy, efficiency, and the quality of generated responses.

---

## Explanation

### Chunking Strategies

**Chunking** refers to dividing large documents into smaller, manageable pieces (chunks) before embedding and storing them in a vector database. The goal is to balance sufficient context per chunk with the need to avoid excessive length (which can hurt retrieval and generation).

**Common chunking approaches:**

- **Fixed-size chunking:** Split text into segments of fixed word, sentence, or token count (e.g., 512 tokens per chunk).
- **Semantic chunking:** Split based on semantic boundaries such as paragraphs, headings, or logical sections.
- **Sliding window:** Overlap chunks by a certain amount to preserve context between them.

**Why is chunking important?**
- Too large: retrieval may miss relevant information or exceed model context limits.
- Too small: loses context, resulting in fragmented or less meaningful retrievals.

### Querying Strategies

**Querying** involves transforming the user's question into a vector (embedding) and searching for the most similar chunks in the database. Strategies impact precision, recall, and speed.

**Key querying considerations:**

- **Embedding model selection:** Use models with strong semantic representation (e.g., OpenAI's `text-embedding-ada-002`, Cohere, or open-source alternatives).
- **Query expansion:** Augment queries with synonyms, keywords, or context variables to improve recall.
- **Conditional logic:** Dynamically adjust queries based on user context or tool outputs (e.g., user role, prior queries).
- **Tool and function interoperability:** Integrate with external tools or APIs to refine or post-process queries and results.

**Ranking and Filtering:**
- Many vector databases (e.g., Pinecone, Weaviate, Chroma) support additional metadata filtering, allowing for hybrid search (combining vector similarity and structured filters).

---

## Examples

### 1. Chunking a Document

```python
from nltk.tokenize import sent_tokenize

def chunk_text(text, max_tokens=200):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    tokens_so_far = 0

    for sentence in sentences:
        tokens = sentence.split()
        if tokens_so_far + len(tokens) > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            tokens_so_far = 0
        current_chunk.append(sentence)
        tokens_so_far += len(tokens)
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

# Example usage
document = "..."  # large document string
chunks = chunk_text(document, max_tokens=150)
```

### 2. Querying a Vector Database (e.g., using Pinecone and OpenAI)

```python
import openai
import pinecone

# Embed the query
query = "How can I reset my password?"
query_embedding = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=query
)["data"][0]["embedding"]

# Query Pinecone for top 3 matches
pinecone.init(api_key="YOUR_API_KEY", environment="us-west1-gcp")
index = pinecone.Index("my-index")
results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

for match in results['matches']:
    print(match['metadata']['text'])
```

### 3. Conditional Querying with Context Variables

```python
def build_query(user_question, context_vars):
    if context_vars.get("user_role") == "admin":
        return f"Admin guide: {user_question}"
    else:
        return user_question

query = build_query("How do I add users?", {"user_role": "admin"})
```

---

## Best Practices

- **Choose chunk size carefully:** Balance chunk length to preserve context without exceeding embedding model limits.
- **Prefer semantic chunking:** Use logical boundaries over arbitrary splits where possible.
- **Deduplicate and clean chunks:** Remove boilerplate or duplicate content before embedding.
- **Leverage metadata:** Store metadata with each chunk for filtering and contextual ranking.
- **Monitor embedding and search quality:** Evaluate both retrieval accuracy (precision, recall) and generation quality.
- **Secure API keys and data:** Ensure sensitive data and credentials are managed appropriately.

**Common pitfalls:**
- Overlapping chunks too much, leading to redundant retrievals.
- Ignoring language nuances (e.g. sentence boundaries) in chunking.
- Using mismatched embedding models for queries and documents.
- Not updating the index after corpus changes.

---

## Related Concepts

- [Retrieval Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)
- [Hybrid Search (combining vector and keyword search)](https://weaviate.io/developers/weaviate/search/hybrid)
- [Tokenization and Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Tool and Function Interoperability](#)
- [Context Variables and Conditional Logic](#)
- [Metadata Filtering in Vector Search](https://docs.pinecone.io/docs/metadata-filtering)

For further reading, see the documentation of your chosen vector database (e.g., [Pinecone](https://docs.pinecone.io/), [Weaviate](https://weaviate.io/), [Chroma](https://docs.trychroma.com/)).