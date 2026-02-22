from langgraph.graph import StateGraph, START, END
from agentic.state import State
from agentic.node.pr import PR_Nodes
from agentic.node.other import if_node_change
from agentic.node.other import if_node_change_node
from agentic.node.other import check_node_dispatcher
from agentic.node.other import check_node_dispatcher_node

graph_builder = StateGraph(State)
graph_builder.add_node("check_node_dispatcher_node", check_node_dispatcher_node)
graph_builder.add_node("if_node_change_node", if_node_change_node)
graph_builder.add_node("greet_run", PR_Nodes.greet_run)
graph_builder.add_node("type_run", PR_Nodes.type_run)


#edge
graph_builder.add_edge(START, "check_node_dispatcher_node")

graph_builder.add_conditional_edges(
    "check_node_dispatcher_node",
    check_node_dispatcher,
    {
        "greet_run": "greet_run",
        "type_run": "type_run",
    }
)

graph_builder.add_conditional_edges(
    "if_node_change_node",
    if_node_change,
    {
        "true_node_change": "check_node_dispatcher_node",
        "false_node_change": END,
    }
)

graph = graph_builder.compile()