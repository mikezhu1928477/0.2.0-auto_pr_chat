import asyncio
import argparse
from graph import build_graph, get_checkpointer
from agentic.state import TestStateInstance
from helper.database import (
    create_session, session_exists, get_session, 
    get_messages, list_sessions, get_retry_count, add_message
)

def print_separator():
    print("━" * 50)

def print_output(creator_id: str, header: str, content: dict):
    """格式化输出"""
    print_separator()
    print(f"{creator_id} | {header}")
    print_separator()
    print()
    for key, value in content.items():
        if value:
            print(f"{key}: {value}")
    print()
    print_separator()

async def cmd_new(creator_id: str):
    """创建新会话，AI发送第一条消息"""
    if session_exists(creator_id):
        print(f"会话已存在: {creator_id}")
        print("使用 'send' 命令继续对话")
        return
    
    # 创建会话
    create_session(
        creator_id=creator_id,
        creator_name=creator_id,
        task=TestStateInstance.task
    )
    
    # 构建状态
    state = {
        "task_informations": {"creator_name": creator_id},
        "task": TestStateInstance.task,
        "settings": {
            "openai_previous_id": None,
            "node_change": True,
            "node_current": "",
            "creator_latest_response": "",
            "ai_latest_response": "",
            "creator_id": creator_id,
            "classification": "",
        }
    }
    
    # 运行图（只运行到第一个节点）
    checkpointer = get_checkpointer()
    graph = build_graph(checkpointer)
    
    config = {"configurable": {"thread_id": creator_id}}
    result = await graph.ainvoke(state, config)
    
    # 输出
    ai_response = result["settings"].get("ai_latest_response", "")
    current_node = result["settings"].get("node_current", "")
    
    print_output(creator_id, f"新会话 | {current_node}", {
        "媒介": ai_response
    })

async def cmd_send(creator_id: str, message: str):
    """发送博主消息，获取AI回复"""
    if not session_exists(creator_id):
        print(f"会话不存在: {creator_id}")
        print("使用 'new' 命令创建新会话")
        return
    
    session = get_session(creator_id)
    if session["status"] != "in_progress":
        print(f"会话已结束: {session['status']}")
        return
    
    # 获取checkpointer和图
    checkpointer = get_checkpointer()
    graph = build_graph(checkpointer)
    
    config = {"configurable": {"thread_id": creator_id}}
    
    # 获取当前状态
    current_state = await graph.aget_state(config)
    
    if current_state.values:
        state = current_state.values
        old_node = state["settings"].get("node_current", "")
    else:
        # 如果没有checkpoint，重新初始化
        state = {
            "task_informations": {"creator_name": creator_id},
            "task": TestStateInstance.task,
            "settings": {
                "openai_previous_id": None,
                "node_change": True,
                "node_current": "",
                "creator_latest_response": "",
                "ai_latest_response": "",
                "creator_id": creator_id,
                "classification": "",
            }
        }
        old_node = ""
    
    # 更新博主消息
    state["settings"]["creator_latest_response"] = message
    
    # 保存博主消息（只保存一次，在这里集中处理）
    current_node = state["settings"].get("node_current", "")
    add_message(creator_id, "human", message, current_node)
    
    # 运行图
    result = await graph.ainvoke(state, config)
    
    # 获取结果
    ai_response = result["settings"].get("ai_latest_response", "")
    new_node = result["settings"].get("node_current", "")
    
    # 检查会话状态
    session = get_session(creator_id)
    status = session["status"]
    
    # 构建header
    if status == "in_progress":
        if old_node and old_node != new_node:
            header = f"{old_node} → {new_node}"
        else:
            header = new_node
    else:
        header = f"{new_node} → 结束 ({status})"
    
    print_output(creator_id, header, {
        "博主": message,
        "媒介": ai_response
    })

def cmd_status(creator_id: str):
    """查看会话状态"""
    if not session_exists(creator_id):
        print(f"会话不存在: {creator_id}")
        return
    
    session = get_session(creator_id)
    
    # 获取重试次数
    nodes = ["greet_run", "type_run", "schedule_run", "product_run", "address_run"]
    retry_info = []
    for node in nodes:
        count = get_retry_count(creator_id, node)
        if count > 0:
            retry_info.append(f"{node}({count})")
    
    print_output(creator_id, "状态", {
        "状态": session["status"],
        "当前节点": session["current_node"] or "-",
        "重试次数": ", ".join(retry_info) if retry_info else "无",
        "创建时间": session["created_at"][:19].replace("T", " "),
        "更新时间": session["updated_at"][:19].replace("T", " "),
    })

def cmd_history(creator_id: str):
    """查看对话历史"""
    if not session_exists(creator_id):
        print(f"会话不存在: {creator_id}")
        return
    
    messages = get_messages(creator_id)
    
    print_separator()
    print(f"{creator_id} | 对话历史")
    print_separator()
    print()
    
    for msg in messages:
        timestamp = msg["timestamp"][11:19] if msg["timestamp"] else ""
        sender = "媒介" if msg["sender"] == "ai" else "博主"
        print(f"[{timestamp}] {sender}: {msg['content']}")
    
    print()
    print_separator()

def cmd_list():
    """列出所有会话"""
    sessions = list_sessions()
    
    print_separator()
    print("所有会话")
    print_separator()
    print()
    print(f"{'创建者':<15} {'状态':<15} {'当前节点':<15} {'更新时间'}")
    print("─" * 50)
    
    for session in sessions:
        creator = session["creator_id"][:12] + "..." if len(session["creator_id"]) > 15 else session["creator_id"]
        status = session["status"]
        node = session["current_node"] or "-"
        updated = session["updated_at"][11:16] if session["updated_at"] else ""
        print(f"{creator:<15} {status:<15} {node:<15} {updated}")
    
    print()
    print_separator()

def main():
    parser = argparse.ArgumentParser(description="PR媒介对话CLI")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # new命令
    new_parser = subparsers.add_parser("new", help="创建新会话")
    new_parser.add_argument("--creator", required=True, help="博主ID")
    
    # send命令
    send_parser = subparsers.add_parser("send", help="发送消息")
    send_parser.add_argument("--creator", required=True, help="博主ID")
    send_parser.add_argument("--message", required=True, help="博主消息")
    
    # status命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    status_parser.add_argument("--creator", required=True, help="博主ID")
    
    # history命令
    history_parser = subparsers.add_parser("history", help="查看历史")
    history_parser.add_argument("--creator", required=True, help="博主ID")
    
    # list命令
    list_parser = subparsers.add_parser("list", help="列出所有会话")
    
    args = parser.parse_args()
    
    if args.command == "new":
        asyncio.run(cmd_new(args.creator))
    elif args.command == "send":
        asyncio.run(cmd_send(args.creator, args.message))
    elif args.command == "status":
        cmd_status(args.creator)
    elif args.command == "history":
        cmd_history(args.creator)
    elif args.command == "list":
        cmd_list()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
