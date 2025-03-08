"""from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
from typing import List, Optional
from dotenv import load_dotenv

# Import Llama Index components
from llama_index.core import SimpleDirectoryReader, StorageContext, ServiceContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_iris import IRISVectorStore

# Create router
router = APIRouter()

# Load environment variables
load_dotenv(override=True)

# Models for request and response
class QueryRequest(BaseModel):
    query: str
    collection_name: str = "default_collection"

class QueryResponse(BaseModel):
    response: str
    source_documents: Optional[List[str]] = None

# IRIS connection parameters
def get_iris_connection_string():
    username = os.getenv('IRIS_USERNAME', 'demo')
    password = os.getenv('IRIS_PASSWORD', 'demo')
    hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
    port = os.getenv('IRIS_PORT', '1972')
    namespace = os.getenv('IRIS_NAMESPACE', 'USER')
    return f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

# Initialize vector store and index
def get_vector_store(collection_name: str):
    connection_string = get_iris_connection_string()
    vector_store = IRISVectorStore.from_params(
        connection_string=connection_string,
        table_name=collection_name,
        embed_dim=1536,  # openai embedding dimension
    )
    return vector_store

# Endpoints
@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        # Check if OpenAI API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            raise HTTPException(status_code=400, detail="OpenAI API key not set")
        
        # Get vector store
        vector_store = get_vector_store(request.collection_name)
        
        # Create index from vector store
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine()
        
        # Execute query
        response = query_engine.query(request.query)
        
        return QueryResponse(
            response=str(response),
            source_documents=None  # Could be populated with source document info if needed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")

@router.post("/index_documents")
async def index_documents(collection_name: str, document_path: str):
    try:
        # Check if OpenAI API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            raise HTTPException(status_code=400, detail="OpenAI API key not set")
        
        # Load documents
        documents = SimpleDirectoryReader(document_path).load_data()
        
        # Get vector store
        vector_store = get_vector_store(collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Create index
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context, 
            show_progress=True,
        )
        
        return {"status": "success", "message": f"Indexed {len(documents)} documents to collection {collection_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {str(e)}")
"""