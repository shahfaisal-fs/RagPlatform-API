import re
from typing import List
from app.services.interfaces.chunk_strategy import ChunkStrategy

def _toklen(s: str) -> int: return max(1, len(s.split()))

class ParagraphChunker(ChunkStrategy):
    async def chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        out, buf = [], ""
        for p in paras:
            cand = (buf + "\n\n" + p).strip() if buf else p
            if _toklen(cand) <= chunk_size:
                buf = cand
            else:
                if buf: out.append(buf)
                tail = " ".join(buf.split()[-max(0,int(_toklen(buf)*chunk_overlap/100)):]) if buf else ""
                buf = (tail + "\n\n" + p).strip()
        if buf: out.append(buf)
        return out
