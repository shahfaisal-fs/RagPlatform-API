'''
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

AZ_SEARCH_ENDPOINT="https://opragsearch.search.windows.net"
AZ_SEARCH_API_KEY="wfkdPsw0rqqDQkgxLNEo7GOLi8KFOF4w6BVcCaJgw3AzSeBfWEHC"
AZ_SEARCH_INDEX="ragdocs"  

# =========================
# Azure OpenAI
# =========================


# --- Configuration ---
# Replace with your Azure AI Search service endpoint and API key
# It's recommended to store these in environment variables for security.

print("Azure AI Search Configuration:")


if not AZ_SEARCH_ENDPOINT or not AZ_SEARCH_API_KEY:
    raise ValueError("Please set the SEARCH_ENDPOINT and SEARCH_API_KEY environment variables.")

# --- Client Initialization ---
credential = AzureKeyCredential(AZ_SEARCH_API_KEY)
search_client = SearchClient(
    endpoint=AZ_SEARCH_ENDPOINT, 
    index_name=AZ_SEARCH_INDEX, 
    credential=credential
)

# --- Performing a Search Query ---
search_text = "luxury hotel" # Your search query

try:
    results = search_client.search(search_text=search_text)

    print(f"Search results for '{search_text}':")
    for result in results:
        # Access document fields based on your index schema
        print(f"  Document ID: {result['id']}, Name: {result['name']}") 
        # You would replace 'id' and 'name' with the actual field names in your index
        
except Exception as e:
    print(f"An error occurred during search: {e}")

# --- Example of creating an index (requires Admin API key) ---
# For index management operations, you would typically use SearchIndexClient
# from azure.search.documents.indexes import SearchIndexClient
# and an Admin API key.
# This example focuses on document search using SearchClient.

'''