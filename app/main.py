from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from app.graph_engine import GraphEngine, Node
from app.workflows import summarization


app = FastAPI(title="Summarization Workflow Engine")


class SummarizationRequest(BaseModel):
    input_text: str


def build_workflow() -> GraphEngine:
    """
    Build the summarization workflow using node-based graph engine.
    """
    graph = GraphEngine()

    # Nodes
    node_split = Node("split_text", summarization.split_text)
    node_summarize = Node("summarize_chunks", summarization.summarize_chunks)
    node_merge = Node("merge_summaries", summarization.merge_summaries)
    node_check = Node("check_length", summarization.check_length)

    # Register nodes
    graph.add_node(node_split)
    graph.add_node(node_summarize)
    graph.add_node(node_merge)
    graph.add_node(node_check)

    # Normal path
    node_split.set_next("summarize_chunks")
    node_summarize.set_next("merge_summaries")
    node_merge.set_next("check_length")

    # Branching logic
    node_check.set_conditional_next({
        "shorten": "split_text",   # loop once if summary too long
        "done": None               # end workflow
    })

    return graph


@app.post("/run-workflow")
def run_workflow(request: SummarizationRequest) -> Dict[str, Any]:
    graph = build_workflow()

    initial_state = {
        "input_text": request.input_text
    }

    result_state = graph.run(initial_state)

    return {
        "final_summary": result_state.data.get("final_summary", "")
    }


@app.get("/")
def home() -> Dict[str, str]:
    return {"message": "Summarization Workflow Engine running!"}
