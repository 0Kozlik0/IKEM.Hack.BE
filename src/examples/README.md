# Llama API Usage Guide

This guide explains how to use the Llama API endpoints for document indexing and querying.

## Prerequisites

1. Make sure the backend server is running
2. Ensure you have the necessary environment variables set:
   - `OPENAI_API_KEY`: Your OpenAI API key for embeddings
   - `IRIS_USERNAME`, `IRIS_PASSWORD`, `IRIS_HOSTNAME`, `IRIS_PORT`, `IRIS_NAMESPACE`: IRIS database connection details

## API Endpoints

### 1. Index Documents

This endpoint indexes documents from a specified directory into a collection.

**Endpoint:** `POST /ikem_api/llama/index_documents`

**Parameters:**
- `collection_name`: Name of the collection to store the documents
- `document_path`: Path to the directory containing the documents

**Example Request:**
```bash
curl -X POST "http://localhost:8000/ikem_api/llama/index_documents?collection_name=my_collection&document_path=/path/to/documents"
```

### 2. Query Documents

This endpoint queries indexed documents using natural language.

**Endpoint:** `POST /ikem_api/llama/query`

**Request Body:**
```json
{
  "query": "Your question here",
  "collection_name": "my_collection"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/ikem_api/llama/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What information can you provide about this topic?", "collection_name": "my_collection"}'
```

## Example Usage

See the `llama_example.py` script for a complete example of how to use these endpoints programmatically. 