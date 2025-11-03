import re
from typing import List
from app.services.interfaces.chunk_strategy import ChunkStrategy

def _toklen(s: str) -> int: return max(1, len(s.split()))

class RecursiveChunker(ChunkStrategy):
    async def chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        sections = re.split(r"\n\s*#{1,6}\s+|^\s*[A-Z][^\n]{0,60}\n[-=]{3,}\s*$", text, flags=re.M)
        chunks, buf = [], ""
        for sec in sections:
            paras = [p.strip() for p in re.split(r"\n\s*\n", sec) if p.strip()]
            for p in paras:
                for s in re.split(r"(?<=[.!?])\s+", p):
                    cand = (buf + " " + s).strip() if buf else s
                    if _toklen(cand) <= chunk_size:
                        buf = cand
                    else:
                        if buf: chunks.append(buf)
                        tail = " ".join(buf.split()[-max(0,int(_toklen(buf)*chunk_overlap/100)):]) if buf else ""
                        buf = (tail + " " + s).strip()
            if buf: chunks.append(buf); buf = ""
        return chunks
