from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from agentic.state import State
from agentic.node.pr import PR_Nodes
from agentic.node.other import initialization
from agentic.node.classifier import classify_response, try_answer_question
from helper.database import add_message, increment_retry_count, update_status, DATABASE_PATH, ensure_database

# 节点顺序映射
NODE_ORDER = ["greet_run", "type_run", "schedule_run", "product_run", "address_run"]

async def classifier_node(state: State):
    """分类器节点：判断博主回复并决定下一步"""
    creator_response = state["settings"].get("creator_latest_response", "")
    
    # 如果没有博主回复，跳过LLM分类调用（节省API费用）
    if not creator_response:
        state["settings"]["classification"] = ""
        return {"settings": state["settings"]}
    
    classification = await classify_response(state)
    state["settings"]["classification"] = classification
    return {"settings": state["settings"]}

async def answer_question_node(state: State):
    """尝试回答博主问题的节点"""
    answer, response_id = await try_answer_question(state)
    
    if "[CANNOT_ANSWER]" in answer:
        # 无法回答，标记为需要人工
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            update_status(creator_id, "escalated")
        state["settings"]["classification"] = "END"
    else:
        # 可以回答，保存回答并继续
        state["settings"]["ai_latest_response"] = answer
        state["settings"]["openai_previous_id"] = response_id
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", answer, state["settings"]["node_current"])
        # 回答后重新分类
        state["settings"]["classification"] = "RETRY"
    return {"settings": state["settings"]}

def route_after_classifier(state: State) -> str:
    """根据分类结果决定下一个节点"""
    classification = state["settings"].get("classification", "")
    current_node = state["settings"]["node_current"]
    creator_id = state["settings"].get("creator_id", "")
    creator_response = state["settings"].get("creator_latest_response", "")
    
    # 如果没有博主回复（初始问候），结束等待博主输入
    if not creator_response:
        return END
    
    if classification == "CONTINUE":
        # 继续到下一个节点
        if current_node in NODE_ORDER:
            current_index = NODE_ORDER.index(current_node)
            if current_index < len(NODE_ORDER) - 1:
                return NODE_ORDER[current_index + 1]
            else:
                if creator_id:
                    update_status(creator_id, "completed")
                return END
        return END
    
    elif classification == "RETRY":
        # 检查重试次数
        retry_count = 0
        if creator_id and current_node:
            retry_count = increment_retry_count(creator_id, current_node)
        
        if retry_count > 3:
            if creator_id:
                update_status(creator_id, "escalated")
            return END
        else:
            return current_node
    
    elif classification == "END":
        if creator_id:
            update_status(creator_id, "refused")
        return END
    
    elif classification == "QUESTION":
        return "answer_question"
    
    return END

def route_after_answer(state: State) -> str:
    """回答问题后的路由"""
    classification = state["settings"].get("classification", "")
    current_node = state["settings"]["node_current"]
    
    if classification == "END":
        return END
    else:
        # 回答后返回当前节点重试
        return current_node if current_node else END

def build_graph(checkpointer=None):
    """构建并编译图"""
    graph_builder = StateGraph(State)

    #nodes
    graph_builder.add_node("initialization", initialization)
    graph_builder.add_node("greet_run", PR_Nodes.greet_run)
    graph_builder.add_node("type_run", PR_Nodes.type_run)
    graph_builder.add_node("schedule_run", PR_Nodes.schedule_run)
    graph_builder.add_node("product_run", PR_Nodes.product_run)
    graph_builder.add_node("address_run", PR_Nodes.address_run)
    graph_builder.add_node("classifier", classifier_node)
    graph_builder.add_node("answer_question", answer_question_node)

    #edge
    graph_builder.add_edge(START, "initialization")
    graph_builder.add_edge("initialization", "greet_run")

    # 每个PR节点后都进入分类器
    graph_builder.add_edge("greet_run", "classifier")
    graph_builder.add_edge("type_run", "classifier")
    graph_builder.add_edge("schedule_run", "classifier")
    graph_builder.add_edge("product_run", "classifier")
    graph_builder.add_edge("address_run", "classifier")

    # 分类器的条件路由
    graph_builder.add_conditional_edges(
        "classifier",
        route_after_classifier,
        {
            "greet_run": "greet_run",
            "type_run": "type_run",
            "schedule_run": "schedule_run",
            "product_run": "product_run",
            "address_run": "address_run",
            "answer_question": "answer_question",
            END: END,
        }
    )

    # 回答问题后的条件路由
    graph_builder.add_conditional_edges(
        "answer_question",
        route_after_answer,
        {
            "greet_run": "greet_run",
            "type_run": "type_run",
            "schedule_run": "schedule_run",
            "product_run": "product_run",
            "address_run": "address_run",
            END: END,
        }
    )

    return graph_builder.compile(checkpointer=checkpointer)

def get_checkpointer():
    """获取SQLite checkpointer"""
    ensure_database()
    return SqliteSaver.from_conn_string(DATABASE_PATH)
