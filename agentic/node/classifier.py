from openai import AsyncOpenAI
from dotenv import load_dotenv
from agentic.state import State
from prompt.classifier_prompt import Classifier_Prompt
from helper.database import get_conversation_history

load_dotenv()
client = AsyncOpenAI()

# 节点目标描述
NODE_GOALS = {
    "greet_run": "获取博主的链接和报价",
    "type_run": "确认合作类型、报价范围、寄品类型",
    "schedule_run": "确认博主的档期",
    "product_run": "让博主选择产品",
    "address_run": "获取博主的收货地址",
}

async def classify_response(state: State) -> str:
    """
    分类博主的回复，决定下一步动作
    
    Returns:
        CONTINUE - 继续到下一个节点
        RETRY - 重试当前节点
        END - 结束对话
        QUESTION - 博主有问题需要回答
    """
    current_node = state["settings"]["node_current"]
    ai_response = state["settings"].get("ai_latest_response", "")
    creator_response = state["settings"]["creator_latest_response"]
    
    # 构建分类输入
    classification_input = f"""
当前节点目标: {NODE_GOALS.get(current_node, "未知")}
AI媒介回复: {ai_response}
博主回复: {creator_response}
"""
    
    llm_output = await client.responses.create(
        model="gpt-4.1",
        input=classification_input,
        instructions=Classifier_Prompt.CLASSIFIER_PROMPT
    )
    
    result = llm_output.output_text.strip().upper()
    
    # 确保返回有效分类
    if result not in ["CONTINUE", "RETRY", "END", "QUESTION"]:
        result = "RETRY"
    
    return result

async def try_answer_question(state: State) -> tuple[str, str]:
    """
    尝试回答博主的问题
    
    Returns:
        tuple[str, str]: (回答内容, OpenAI response ID)
            - 回答内容：LLM的回答，或包含 [CANNOT_ANSWER] 如果无法回答
            - response_id：用于保持对话上下文
    """
    creator_id = state["settings"].get("creator_id", "")
    conversation_history = ""
    
    if creator_id:
        conversation_history = get_conversation_history(creator_id)
    
    question = state["settings"]["creator_latest_response"]
    
    llm_output = await client.responses.create(
        model="gpt-4.1",
        input="请回答博主的问题",
        previous_response_id=state["settings"]["openai_previous_id"],
        instructions=Classifier_Prompt.ANSWER_QUESTION_PROMPT.format(
            conversation_history=conversation_history,
            question=question
        )
    )
    
    return llm_output.output_text, llm_output.id
