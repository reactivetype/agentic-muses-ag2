# ChromaDB PGVector Qdrant MongoDB integrations

## Overview

**Retrieval Augmented Generation (RAG)** combines large language models (LLMs) with external knowledge sources to create agents capable of dynamic, context-aware answers. Central to RAG is the use of **vector databases** for semantic search—storing document embeddings and enabling similarity-based retrieval.

Four prominent vector database solutions are:

- **ChromaDB**: An open-source embedding database optimized for LLM applications.
- **PGVector**: A PostgreSQL extension bringing vector search into the relational database world.
- **Qdrant**: A high-performance, production-ready vector search engine.
- **MongoDB**: A NoSQL document database with vector search capabilities (Atlas Search).

This chapter explores how to integrate, query, and manage these vector databases, focusing on RAG workflows, chunking/tokenization, and interoperability.

---

## Explanation

### 1. Retrieval Augmented Generation (RAG) with Vector Stores

RAG agents enhance LLM responses by retrieving relevant document chunks from a vector database, using context variables to tailor queries and conditional logic to orchestrate retrieval and generation steps.

#### Workflow

1. **Ingestion**: Documents are split into smaller chunks, embedded (vectorized) using a model (e.g., OpenAI, Sentence Transformers), and stored in a vector database.
2. **Querying**: A user query is embedded, then a similarity search retrieves the most relevant chunks.
3. **Augmentation**: Retrieved chunks are fed to the LLM as context for answer generation.

### 2. Integration Patterns

- **ChromaDB**: Pure Python, simple to set up, ideal for prototyping and small-scale deployments.
- **PGVector**: Integrates into existing PostgreSQL infrastructure, supports SQL queries and ACID transactions.
- **Qdrant**: Offers REST/gRPC APIs, high performance for large datasets, supports filtering and metadata.
- **MongoDB**: Leverages Atlas Search for vector similarity, integrates with document-based data models.

### 3. Chunking and Tokenization

- **Chunking**: Splitting documents into manageable pieces (by sentences, paragraphs, or token count).
- **Tokenization**: Ensuring chunks fit within model/token limits to optimize retrieval and context window usage.

---

## Examples

### 1. ChromaDB Integration

```python
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection("documents")

# Embed and add documents
embedder = SentenceTransformer('all-MiniLM-L6-v2')
texts = ["LLMs are powerful.", "Vector databases enable semantic search."]
embeddings = embedder.encode(texts)

for text, embedding in zip(texts, embeddings):
    collection.add(
        documents=[text],
        embeddings=[embedding.tolist()],
        ids=[str(hash(text))]
    )

# Query
query = "How do vector databases work?"
query_embedding = embedder.encode([query])[0]
results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=2)
print(results)
```

### 2. PGVector Integration

```python
import psycopg2
import numpy as np

# Connect to PostgreSQL with PGVector installed
conn = psycopg2.connect("dbname=vector_db user=postgres password=secret")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);
""")
conn.commit()

# Insert document
embedding = np.random.rand(384).tolist()
cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", ("My doc text", embedding))
conn.commit()

# Similarity search
query_embedding = np.random.rand(384).tolist()
cur.execute("""
SELECT content FROM documents
ORDER BY embedding <-> %s LIMIT 5
""", (query_embedding,))
print(cur.fetchall())
```

### 3. Qdrant Integration

```python
import qdrant_client
from sentence_transformers import SentenceTransformer

client = qdrant_client.QdrantClient("localhost", port=6333)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Create collection
client.recreate_collection(
    collection_name="docs",
    vector_size=384,
    distance="Cosine"
)

# Add vectors
texts = ["Qdrant is fast.", "Supports filtering."]
embeddings = embedder.encode(texts)
points = [
    qdrant_client.models.PointStruct(
        id=i, vector=embedding.tolist(), payload={"text": text}
    ) for i, (text, embedding) in enumerate(zip(texts, embeddings))
]
client.upsert(collection_name="docs", points=points)

# Search
query = "Does Qdrant support filtering?"
query_vec = embedder.encode([query])[0]
results = client.search(collection_name="docs",
                        query_vector=query_vec.tolist(),
                        limit=2)
print([hit.payload['text'] for hit in results])
```

### 4. MongoDB Atlas Vector Search (Python, PyMongo)

```python
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb+srv://user:pass@cluster0.mongodb.net")
db = client['vector_db']
collection = db['documents']

embedder = SentenceTransformer('all-MiniLM-L6-v2')
text = "MongoDB supports vector search."
embedding = embedder.encode([text])[0].tolist()

# Insert document with embedding
collection.insert_one({"text": text, "embedding": embedding})

# Vector search (Atlas Search via $search)
query = "How does vector search work in MongoDB?"
query_embedding = embedder.encode([query])[0].tolist()

pipeline = [
    {
        "$search": {
            "index": "vector_index",
            "knnBeta": {
                "vector": query_embedding,
                "path": "embedding",
                "k": 3
            }
        }
    }
]
results = list(collection.aggregate(pipeline))
print([doc['text'] for doc in results])
```

---

## Best Practices

- **Consistent Embedding Model**: Use the same embedding model for both storage and query to ensure semantic alignment.
- **Chunking Strategy**: Balance chunk size—too large reduces retrieval granularity; too small may split context.
- **Metadata Indexing**: Store metadata (e.g., source, tags) alongside vectors for filtered and conditional retrieval.
- **Batch Operations**: Batch inserts and queries for efficiency, especially with large datasets.
- **Token Limits Awareness**: Ensure retrieved chunks fit within the LLM's context window.
- **Security and Access Control**: Secure database endpoints; handle sensitive data appropriately.
- **Monitoring & Logging**: Track retrieval performance and query patterns for optimization.

**Pitfalls to avoid:**

- Mismatched embedding dimensions or models between ingestion and query.
- Ignoring text preprocessing (tokenization, normalization).
- Overloading context window in LLMs, leading to truncation.
- Neglecting database scaling and backup strategies.

---

## Related Concepts

- [Retrieval Augmented Generation (RAG)](https://huggingface.co/docs/transformers/main/en/main_classes/retrieval)
- [Embeddings and Semantic Search](https://platform.openai.com/docs/guides/embeddings)
- [Chunking and Tokenization Strategies](https://www.sbert.net/examples/applications/semantic-search/README.html)
- [LangChain Vector Store Integrations](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PGVector Documentation](https://github.com/pgvector/pgvector)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-search/vector-search/)
- [Tool and Function Interoperability in RAG](https://python.langchain.com/docs/modules/agents/tools/)
- [Context Variables and Conditional Logic](https://python.langchain.com/docs/expression_language/how_to/context_variables/)