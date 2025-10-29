from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import ChunkStrategy
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RecursiveChunkStrategy(ChunkStrategy):
    async def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into chunks using RecursiveCharacterTextSplitter"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        return chunks