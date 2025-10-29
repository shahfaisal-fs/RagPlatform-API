from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import DocumentProcessor
from langchain_community.document_loaders import UnstructuredFileLoader
from io import BytesIO
import tempfile
import os

class UnstructuredDocumentProcessor(DocumentProcessor):
    async def process_document(self, file_content: bytes, metadata: Dict[str, Any]) -> str:
        """Process document using Unstructured"""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.flush()
            
            try:
                loader = UnstructuredFileLoader(temp_file.name)
                documents = loader.load()
                return "\n".join([doc.page_content for doc in documents])
            finally:
                os.unlink(temp_file.name)
                
        return ""