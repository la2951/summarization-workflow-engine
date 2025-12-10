from typing import Dict, Any, List
from app.graph_engine import GraphState


def _chunk_text(text: str, size: int = 200) -> List[str]:
    if not text:
        return []
    return [text[i:i + size] for i in range(0, len(text), size)]


def split_text(state: GraphState) -> Dict[str, Any]:
    """
    Node 1: Split input text into smaller chunks.
    """
    text = state.data.get("input_text", "")
    chunks = _chunk_text(text, 200)
    return {"chunks": chunks}


def summarize_chunks(state: GraphState) -> Dict[str, Any]:
    """
    Node 2: Summarize each text chunk (simple rule-based summary).
    """
    chunks = state.data.get("chunks", [])
    summaries = []

    for c in chunks:
        sentences = [s.strip() for s in c.split(".") if s.strip()]
        summary = ". ".join(sentences[:2])  # take first 2 sentences
        summaries.append(summary)

    return {"summaries": summaries}


def merge_summaries(state: GraphState) -> Dict[str, Any]:
    """
    Node 3: Merge all summaries into one final summary.
    """
    summaries = state.data.get("summaries", [])
    merged = " ".join(summaries)
    return {"final_summary": merged}


def check_length(state: GraphState) -> Dict[str, Any]:
    """
    Node 4 (Branching):
    If final summary > 200 chars, shorten and loop once.
    Otherwise, finish.
    """
    summary = state.data.get("final_summary", "") or ""

    if len(summary) > 200:
        shortened = summary[:200]
        return {
            "decision": "shorten",
            "input_text": shortened
        }

    return {"decision": "done"}
