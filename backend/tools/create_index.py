#!/usr/bin/env python3
"""
Create (or recreate) an Azure Cognitive Search index
with vector search + multi-tenant metadata support.

Usage:
    python tools/create_index.py [--index NAME] [--force]
"""

import os
import argparse
import json
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

API_VERSION = "2023-11-01"  # using latest stable version


def get_env(var: str, required: bool = True):
    v = os.getenv(var)
    if required and not v:
        print(f"Missing required environment variable: {var}")
        sys.exit(1)
    return v


def index_exists(endpoint: str, api_key: str, index_name: str) -> bool:
    url = f"{endpoint}/indexes/{index_name}?api-version={API_VERSION}"
    r = requests.get(url, headers={"api-key": api_key})
    return r.status_code == 200


def delete_index(endpoint: str, api_key: str, index_name: str):
    url = f"{endpoint}/indexes/{index_name}?api-version={API_VERSION}"
    r = requests.delete(url, headers={"api-key": api_key})
    print(f"Deleted index {index_name}" if r.status_code in (200, 204) else r.text)


def create_index(endpoint: str, api_key: str, index_name: str):
    # Embedding dimension MUST match selected AOAI embedding model —
    # update if you use text-embedding-3-large (3072 dims)
    EMBEDDING_DIM = 1536  # for text-embedding-3-small

    body = {
    "name": index_name,
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
        {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True},
        {"name": "source", "type": "Edm.String", "filterable": True, "retrievable": True},
        {"name": "tenant", "type": "Edm.String", "filterable": True, "facetable": True, "retrievable": True},
        {"name": "department", "type": "Edm.String", "filterable": True, "retrievable": True},
        {"name": "project_id", "type": "Edm.String", "filterable": True, "retrievable": True},
        # NEW — Personal and Shared RBAC ✅
        {"name": "visibility", "type": "Edm.String", "filterable": True, "retrievable": True},
        {"name": "owner_user_id", "type": "Edm.String", "filterable": True, "retrievable": True},
        {
            "name": "group_ids",
            "type": "Collection(Edm.String)",
            "filterable": True,
            "retrievable": True
        },

        # Data protection
        {"name": "classification", "type": "Edm.String", "filterable": True, "retrievable": True},

            
        # ✅ VECTOR FIELD — new API syntax
        {
            "name": "content_vector",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "retrievable": True,
            "dimensions": 1536,
            "vectorSearchProfile": "default-profile"
        },

        # ✅ optional metadata string
        {"name": "content_vector_metadata", "type": "Edm.String", "retrievable": True}
    ],

    # ✅ MUST use this layout for vector search
    "vectorSearch": {
        "profiles": [
            {
                "name": "default-profile",
                "algorithm": "default-hnsw"
            }
        ],
        "algorithms": [
            {
                "name": "default-hnsw",
                "kind": "hnsw",
                "hnswParameters": {
                    "metric": "cosine",
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500
                }
            }
        ]
    }
}




    url = f"{endpoint}/indexes/{index_name}?api-version={API_VERSION}"
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    r = requests.put(url, headers=headers, json=body)

    if r.status_code in (200, 201):
        print(f"✅ Index '{index_name}' created successfully!")
    else:
        print(f"❌ Failed to create index: {r.status_code}")
        print(r.text)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create Azure Search RAG index")
    parser.add_argument("--index", help="Override index name")
    parser.add_argument("--force", action="store_true", help="Delete and recreate index")
    args = parser.parse_args()

    endpoint = get_env("AZ_SEARCH_ENDPOINT")
    api_key = get_env("AZ_SEARCH_API_KEY")
    index_name = args.index or get_env("AZ_SEARCH_INDEX")

    print(f"Using Search endpoint: {endpoint}")
    print(f"Index: {index_name}")

    if index_exists(endpoint, api_key, index_name):
        if not args.force:
            print(f"Index already exists. Re-run with --force to recreate.")
            return
        else:
            delete_index(endpoint, api_key, index_name)

    create_index(endpoint, api_key, index_name)


if __name__ == "__main__":
    main()
