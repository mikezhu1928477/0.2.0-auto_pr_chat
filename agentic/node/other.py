import json
from agentic.state import State

def check_node_dispatcher_node(state: State):
    return{}

def if_node_change_node(state: State):
    return{}

def check_node_dispatcher(state: State):
    current_node = state["settings"]["node_current"]
    return current_node


def if_node_change(state: State) -> dict:
    NODE_ORDER = ["greet_run", "type_run", "schedule_run", "product_run", "address_run"]
    if not state["settings"]["node_change"]:
        return "false_node_change"
    
    current = state["settings"]["node_current"]
    current_index = NODE_ORDER.index(current)
    next_node = NODE_ORDER[current_index + 1]
    
    state["settings"]["node_current"] = next_node
    state["settings"]["node_change"] = False
    
    return "true_node_change"