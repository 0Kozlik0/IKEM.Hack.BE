import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000/ikem_api/llama"

def index_documents(collection_name, document_path):
    """
    Index documents from a directory into a collection
    """
    url = f"{BASE_URL}/index_documents"
    params = {
        "collection_name": collection_name,
        "document_path": document_path
    }
    
    response = requests.post(url, params=params)
    print(f"Indexing response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def query_documents(collection_name, query_text):
    """
    Query documents from a collection
    """
    url = f"{BASE_URL}/query"
    data = {
        "query": query_text,
        "collection_name": collection_name
    }
    
    response = requests.post(url, json=data)
    print(f"Query response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    # Example usage
    collection_name = "example_collection"
    document_path = "../data/example_docs"  # Path to your documents
    
    # First, index some documents
    print("Indexing documents...")
    index_documents(collection_name, document_path)
    
    # Then, query the indexed documents
    print("\nQuerying documents...")
    query_text = "What information can you provide about this topic?"
    query_documents(collection_name, query_text) 