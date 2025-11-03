from typing import Dict, Any
from app.services.pipeline.strategy_registry import StrategyRegistry



class ServiceContainer:

    def __init__(self, pipeline: Dict[str, Any]):
        self.pipeline = pipeline or {}

        def load(key: str, registry: Dict[str, Any]):
            name = self.pipeline.get(key)
            if name in registry:
                return registry[name]()
            return next(iter(registry.values()))()  # default

        self.chunker = load("chunker", StrategyRegistry.chunkers)
        self.embedder = load("embedder", StrategyRegistry.embedders)
        self.store = load("vector_store", StrategyRegistry.stores)
        self.pii = load("pii", StrategyRegistry.pii)
        self.gov = load("governance", StrategyRegistry.governance)
        self.rerank = load("reranker", StrategyRegistry.rerankers)
        self.llm = load("llm", StrategyRegistry.llms)
        self.pseudo   = load("pseudonymizer", StrategyRegistry.pseudonymizers)

    def params(self) -> Dict[str, Any]:
        return {
            "chunk_size": self.pipeline.get("chunk_size", 800),
            "chunk_overlap": self.pipeline.get("chunk_overlap", 100)
        }
