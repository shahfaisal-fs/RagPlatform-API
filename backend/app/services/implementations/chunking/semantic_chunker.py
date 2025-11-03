import re, numpy as np
from typing import List
from app.services.interfaces.chunk_strategy import ChunkStrategy
from app.services.interfaces.embedding_strategy import EmbeddingStrategy


def _toklen(s: str) -> int:
    return max(1, len(s.split()))


class SemanticChunker(ChunkStrategy):
    def __init__(self, embedder: EmbeddingStrategy, sim_threshold: float = 0.78):
        self.embedder = embedder
        self.sim_threshold = sim_threshold

    async def chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        if not paras:
            return []

        vecs = await self.embedder.embed_texts(paras)  # ✅ No import from registry

        def cos(a, b):
            a, b = np.array(a), np.array(b)
            div = (np.linalg.norm(a) * np.linalg.norm(b)) or 1.0
            return float(np.dot(a, b) / div)

        chunks = []
        curr, curr_vec = paras[0], vecs[0]

        for i in range(1, len(paras)):
            sim = cos(curr_vec, vecs[i])
            cand = (curr + "\n\n" + paras[i]).strip()
            if sim >= self.sim_threshold and _toklen(cand) <= chunk_size:
                curr = cand
                curr_vec = (np.array(curr_vec) + np.array(vecs[i])).tolist()
            else:
                chunks.append(curr)
                tail_tokens = max(1, int(_toklen(curr) * chunk_overlap / 100))
                tail = " ".join(curr.split()[-tail_tokens:])
                curr = (tail + "\n\n" + paras[i]).strip()
                curr_vec = vecs[i]

        if curr:
            chunks.append(curr)

        return chunks
