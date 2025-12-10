from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from app.graph_engine import GraphEngine, Node
from app.workflows import summarization


app = FastAPI(title="Summarization Workflow Engine")


class SummarizationRequest(BaseModel):
    input_text: str


def build_workflow() -> GraphEngine:
    graph = GraphEngine()

    node_split = Node("split_text", summarization.split_text)
    node_summarize = Node("summarize_chunks", summarization.summarize_chunks)
    node_merge = Node("merge_summaries", summarization.merge_summaries)

    graph.add_node(node_split)
    graph.add_node(node_summarize)
    graph.add_node(node_merge)

    node_split.set_next("summarize_chunks")
    node_summarize.set_next("merge_summaries")
    node_merge.set_next(None)

    return graph


@app.post("/run-workflow")
def run_workflow(request: SummarizationRequest) -> Dict[str, Any]:
    graph = build_workflow()
    result = graph.run({"input_text": request.input_text})
    return {"final_summary": result.data.get("final_summary", "")}
