from typing import Callable, Dict, Optional, Any


class GraphState:
    """
    Holds the mutable state that flows between nodes.
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data: Dict[str, Any] = data or {}

    def update(self, new_data: Dict[str, Any]) -> None:
        """
        Merge new key/value pairs into the state.
        """
        if not new_data:
            return
        self.data.update(new_data)


class Node:
    """
    Represents a single step in the workflow.
    - name: unique identifier
    - task: function that takes GraphState and returns dict
    - next_node: normal next node
    - conditional_next: mapping from decision -> next node
    """
    def __init__(self, name: str, task: Callable[['GraphState'], Dict[str, Any]]):
        self.name = name
        self.task = task
        self.next_node: Optional[str] = None
        self.conditional_next: Optional[Dict[str, str]] = None

    def set_next(self, node_name: str) -> None:
        self.next_node = node_name

    def set_conditional_next(self, condition_map: Dict[str, str]) -> None:
        self.conditional_next = condition_map


class GraphEngine:
    """
    Simple workflow engine:
    - stores nodes
    - knows start node
    - runs nodes in sequence
    - supports conditional branching & looping
    """
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.start_node: Optional[str] = None

    def add_node(self, node: Node) -> None:
        self.nodes[node.name] = node
        if self.start_node is None:
            self.start_node = node.name

    def run(self, initial_state: Dict[str, Any], max_steps: int = 20) -> GraphState:
        """
        Execute the graph starting from start_node.

        max_steps is a hard safety limit to avoid infinite loops.
        """
        state = GraphState(initial_state)
        current_name = self.start_node
        steps = 0

        while current_name is not None and steps < max_steps:
            node = self.nodes[current_name]

            # Execute node logic
            output = node.task(state)
            state.update(output)

            # Decide the next node
            if node.conditional_next:
                decision = output.get("decision")
                current_name = node.conditional_next.get(decision)
            else:
                current_name = node.next_node

            steps += 1

        return state

