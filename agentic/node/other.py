from agentic.state import State
from helper.database import create_session, session_exists

async def initialization(state: State):
    """初始化会话，创建数据库记录"""
    creator_id = state["settings"].get("creator_id", "")
    creator_name = state["task_informations"].get("creator_name", "unknown")
    
    if creator_id and not session_exists(creator_id):
        create_session(
            creator_id=creator_id,
            creator_name=creator_name,
            task=state["task"]
        )
    return {"settings": state["settings"]}
