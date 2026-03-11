from langgraph.graph import StateGraph, START, END
from agentic.state import State
from agentic.node.pr import PR_Nodes
from agentic.node.other import (
    if_node_change, if_node_change_node, 
    check_node_dispatcher, check_node_dispatcher_node
)

graph_builder = StateGraph(State)
#---------------------------------------------------------node
graph_builder.add_node("greet_run", PR_Nodes.greet_run)
graph_builder.add_node("type_run", PR_Nodes.type_run)
graph_builder.add_node("schedule_run", PR_Nodes.schedule_run)
graph_builder.add_node("product_run", PR_Nodes.product_run)
graph_builder.add_node("address_run", PR_Nodes.address_run)
#---------------------------------------------------------conditional edge node
graph_builder.add_node("check_node_dispatcher_node", check_node_dispatcher_node)
graph_builder.add_node("if_node_change_node", if_node_change_node)

#edge
graph_builder.add_edge(START, "check_node_dispatcher_node")
graph_builder.add_edge("greet_run", "if_node_change_node")
graph_builder.add_edge("type_run", "if_node_change_node")
graph_builder.add_edge("schedule_run", "if_node_change_node")
graph_builder.add_edge("product_run", "if_node_change_node")
graph_builder.add_edge("address_run", "if_node_change_node")

#conditional edge
graph_builder.add_conditional_edges(
    "check_node_dispatcher_node",
    check_node_dispatcher,
    {
        "greet_run": "greet_run",
        "type_run": "type_run",
        "schedule_run": "schedule_run",
        "product_run": "product_run",
        "address_run": "address_run",
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

#compile()
graph = graph_builder.compile()