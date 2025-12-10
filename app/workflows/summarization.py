from typing import Dict, Any, List
from app.graph_engine import GraphState


def _chunk_text(text: str, size: int) -> List[str]:
    if not text:
        return []
    return [text[i:i + size] for i in range(0, len(text), size)]


def split_text(state: GraphState) -> Dict[str, Any]:
    text = state.data.get("input_text", "")
    chunks = _chunk_text(text, 200)
    return {"chunks": chunks}


def summarize_chunks(state: GraphState) -> Dict[str, Any]:
    chunks = state.data.get("chunks", [])
    summaries: List[str] = []
    for c in chunks:
        sentences = c.split(".")
        summary = ". ".join(sentences[:2])
        summaries.append(summary.strip())
    return {"summaries": summaries}


def merge_summaries(state: GraphState) -> Dict[str, Any]:
    summaries = state.data.get("summaries", [])
    merged = " ".join(summaries)
    return {"final_summary": merged.strip()}
