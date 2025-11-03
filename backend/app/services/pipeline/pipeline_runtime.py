import base64
import hashlib
from typing import Dict, Any, List
import logging

from sqlalchemy.orm import Session

from app.models.governance.ingestionlog import IngestionLog
from app.models.governance.piientity import PIIEntity
from app.models.governance.policydecision import PolicyDecision
from app.services.interfaces.pii_detector import PIIDetector
from app.services.interfaces.pseudonymizer import Pseudonymizer
logger = logging.getLogger(__name__)

DEFAULT_POLICY = {
    "allowed_classifications": ["Public", "Internal"],  # Confidential needs justification
    "require_owner": True  # document must have an owner user ID
}

def base_id(raw: str) -> str:
    """
    Deterministic ID generator.
    Converts raw text to a short base64 hash, safe for Azure Search.
    """
    h = hashlib.sha256(raw.encode()).digest()
    return base64.urlsafe_b64encode(h[:12]).decode().rstrip("=")

class PipelineRuntime:
    """
    Orchestrates: PII -> Governance -> Chunk -> Embed -> Store
    and: Embed Query -> Search -> Rerank -> LLM synth
    """
    @staticmethod
    #async def ingest(container, text: str, meta: Dict[str, Any],db: Session) -> int:
    async def ingest(container, text: str, meta: Dict[str, Any]) -> int:

        # PII + Governance
        pii: PIIDetector = container.pii
        pseudo: Pseudonymizer = container.pseudo
        findings = await pii.detect_pii(text)
        pii_summary = {}
        for f in findings:
            pii_summary[f["type"]] = pii_summary.get(f["type"], 0) + 1

        decision = "allow"
        reason = "no_pii"
        masked_text = text
        if findings:
            if meta.get("visibility","Shared") == "Public" and DEFAULT_POLICY in ("strict_public",):
                decision = "block"
                reason = "pii_found_in_public"
            else:
                # Pseudonymize (reversible)
                masked_text, token_map = await pseudo.tokenize(text, findings)
                decision = "mask"
                reason = "pii_masked"

                # Persist token map (encrypted values) once per doc key base
                '''
                base_key = f"{meta['tenant']}-{meta['project_id']}"
                for tm in token_map:
                    enc = await pseudo.encrypt(tm["raw"])
                    db.add(PIIEntity(doc_key=base_key, token_id=tm["token"], entity_type=tm["type"], raw_encrypted=enc))
                '''
        '''
        db.add(PolicyDecision(
            tenant_id=meta["tenant"], project_id=meta["project_id"],
            rule="block_public_with_pii" if decision=="block" else "mask_pii",
            decision="blocked" if decision=="block" else "allowed",
            reason=reason,
            context={"visibility": meta.get("visibility"), "pii_summary": pii_summary}
        ))
        db.flush()
        '''
        if decision == "block":
            '''
            # Also record ingestion attempt
            db.add(IngestionLog(
                tenant_id=meta["tenant"],
                project_id=meta["project_id"],
                department=meta["department"],
                source_system=meta.get("source","Upload"),
                visibility=meta.get("visibility"),
                classification=meta.get("classification","Internal"),
                owner_user_id=meta.get("user_id","unknown"),
                groups=meta.get("allowed_group_ids", []),
                doc_key=f"{meta['tenant']}-{meta['project_id']}",
                chunk_count=0,
                pii_found=True,
                pii_summary=pii_summary,
                policy_decision="blocked"
            ))
            db.commit()
            '''
            return 0
        p = container.params()
        chunks = await container.chunker.chunk_text(masked_text, p["chunk_size"], p["chunk_overlap"])
        if not chunks:
            return 0

        embs = await container.embedder.embed_texts(chunks)
        logger.info(f"Generated {len(embs)} embeddings for {len(chunks)} chunks.")
        metadata_list: List[Dict[str,Any]] = []
        for idx, c in enumerate(chunks):
            metadata_list.append({
                "id": f"{meta['project_id']}-{idx}",
                "tenant": meta["tenant"],
                "project_id": meta["project_id"],
                "department": meta["department"],
                "source": meta.get("source", "Upload"),
                "classification": meta.get("classification", "Internal"),
                "visibility": meta.get("visibility", "Shared"),
                "group_ids": meta.get("group_ids", []),
                "owner_user_id": meta.get("owner_user_id", "unknown")
            })

        await container.store.add_embeddings(chunks, embs, metadata_list)

        '''
        # Record ingestion log
        db.add(IngestionLog(
            tenant_id=meta["tenant"],
            project_id=meta["project_id"],
            department=meta["department"],
            source_system=meta.get("source","Upload"),
            visibility=meta.get("visibility"),
            classification=meta.get("classification","Internal"),
            owner_user_id=meta.get("user_id","unknown"),
            groups=meta.get("allowed_group_ids", []),
            doc_key=base_id,
            chunk_count=len(chunks),
            pii_found=bool(findings),
            pii_summary=pii_summary,
            policy_decision="masked" if decision=="mask" else "allowed"
        ))
        db.commit()
        '''
        logger.info(f"Ingestion complete: {len(chunks)} chunks -> {meta['project_id']}")
        return len(chunks)

    

    @staticmethod
    async def answer(container, query: str, meta: Dict[str, Any], top_k: int) -> Dict[str, Any]:
        logger.info(f"Answer pipeline started: Query = {query}")

        # ✅ Step 1: Embed the query
        qv = (await container.embedder.embed_texts([query]))[0]

        # ✅ Step 2: Filter only same tenant/project
        filter_expr = f"tenant eq '{meta['tenant']}' "
        f"and project_id eq '{meta['project_id']}' "
        f"and ("
        f"visibility eq 'Public' "
        f"or (visibility eq 'Shared' and group_ids/any(g: search.in(g, '{','.join(meta['group_ids'])}'))) "
        f"or (visibility eq 'Private' and owner_user_id eq '{meta['owner_user_id']}')"
        f")"
        logger.info(f"Vector search filter: {filter_expr}")

        # ✅ Step 3: Vector Search Retrieve
        hits = await container.store.search(qv, top_k, filter_expr)
        logger.info(f"Vector search returned {len(hits)} hits")

        if not hits:
            return {"answer": "No relevant content found.", "sources": []}

        # ✅ Step 4: Optional Reranking
        if hasattr(container, "rerank") and container.rerank:
            hits = await container.rerank.rerank(qv, hits)
            logger.info("Reranking applied")

        # ✅ Step 5: Build LLM context
        ctx = "\n\n".join([f"[{i+1}] {h['content']}" for i, h in enumerate(hits[:5])])
        sys_prompt = (
            "You are an enterprise assistant. "
            "Use ONLY the provided context. If not present, say you don't know. "
            "Cite sources like [1],[2]."
        )
        user_prompt = f"Context:\n{ctx}\n\nQuestion: {query}\nAnswer concisely with citations."

        # ✅ Step 6: Generate response
        logger.info("Calling LLM with context")
        answer_text = await container.llm.generate(sys_prompt, user_prompt)

        return {"answer": answer_text, "sources": hits[:5]}

