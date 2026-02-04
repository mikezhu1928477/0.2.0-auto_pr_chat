from langgraph.graph import StateGraph, START, END
from agentic.state import State
from agentic.node.pr import PR_Nodes
from agentic.node.other import initialization

graph_builder = StateGraph(State)
graph_builder.add_node("initialization", initialization)
graph_builder.add_node("greet_run", PR_Nodes.greet_run)
graph_builder.add_node("type_run", PR_Nodes.type_run)
graph_builder.add_node("schedule_run", PR_Nodes.schedule_run)
graph_builder.add_node("product_run", PR_Nodes.product_run)
graph_builder.add_node("address_run", PR_Nodes.address_run)

#edge
graph_builder.add_edge(START, "initialization")
graph_builder.add_edge("initialization", "greet_run")
graph_builder.add_edge("greet_run", "type_run")
graph_builder.add_edge("type_run", "schedule_run")
graph_builder.add_edge("schedule_run", "product_run")
graph_builder.add_edge("product_run", "address_run")
graph_builder.add_edge("address_run", END)

graph = graph_builder.compile()
