from typing import Dict, Any
from app.services.pipeline.strategy_registry import StrategyRegistry

class PipelineBuilder:

    @staticmethod
    def build(config: Dict[str, Any]):
        """Builds the pipeline services selected by user/project."""
        
        return {
            "chunker": StrategyRegistry.chunkers[config["chunker"]](),
            "embedder": StrategyRegistry.embedders[config["embedder"]](),
            "vector": StrategyRegistry.stores[config["vector_store"]](),
            "pii": StrategyRegistry.pii[config["pii_detector"]](),
            "governance": StrategyRegistry.governance[config["governance"]](),
            "rerank": StrategyRegistry.rerankers[config["reranker"]](),
            "llm": StrategyRegistry.llms[config["llm"]](),
        }
