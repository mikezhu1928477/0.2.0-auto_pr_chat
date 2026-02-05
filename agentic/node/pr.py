from openai import AsyncOpenAI
from dotenv import load_dotenv
import inspect
from agentic.state import State
from prompt.pr_prompt import PR_Prompt
from helper.database import add_message
load_dotenv()           
client = AsyncOpenAI()

class PR_Nodes:

    async def greet_run(state: State):
        llm_output = await client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE1_PROMPT
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = llm_output.output_text

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id
        state["settings"]["node_current"] = inspect.currentframe().f_code.co_name
        state["settings"]["ai_latest_response"] = llm_output.output_text
        
        #存储对话（只存AI消息，人类消息在cmd_send中统一保存）
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", llm_output.output_text, "greet_run")

        return {"settings": state["settings"]}
    
    async def type_run(state: State):
        llm_output = await client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE2_PROMPT.format( #llm在此node里需要的外部信息
                price=state["task"][0]["maximum_price"],
                collab_type=state["task"][0]["collab_type"],
                delivery_type=state["task"][0]["delivery_type"]
            )
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = llm_output.output_text

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id
        state["settings"]["node_current"] = inspect.currentframe().f_code.co_name
        state["settings"]["ai_latest_response"] = llm_output.output_text
        
        #存储对话（只存AI消息，人类消息在cmd_send中统一保存）
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", llm_output.output_text, "type_run")

        return {"settings": state["settings"]}
    
    async def schedule_run(state: State):
        llm_output = await client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE3_PROMPT.format(
                schedule=state["task"][0]["schedule"]
            )
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = llm_output.output_text

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id
        state["settings"]["node_current"] = inspect.currentframe().f_code.co_name
        state["settings"]["ai_latest_response"] = llm_output.output_text
        
        #存储对话（只存AI消息，人类消息在cmd_send中统一保存）
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", llm_output.output_text, "schedule_run")

        return {"settings": state["settings"]}
    
    async def product_run(state: State):
        llm_output = await client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE4_PROMPT.format(
                product=state["task"][0]["product"]
            )
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = llm_output.output_text

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id
        state["settings"]["node_current"] = inspect.currentframe().f_code.co_name
        state["settings"]["ai_latest_response"] = llm_output.output_text
        
        #存储对话（只存AI消息，人类消息在cmd_send中统一保存）
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", llm_output.output_text, "product_run")

        return {"settings": state["settings"]}
    
    async def address_run(state: State):
        llm_output = await client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE5_PROMPT
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = llm_output.output_text

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id
        state["settings"]["node_current"] = inspect.currentframe().f_code.co_name
        state["settings"]["ai_latest_response"] = llm_output.output_text
        
        #存储对话（只存AI消息，人类消息在cmd_send中统一保存）
        creator_id = state["settings"].get("creator_id", "")
        if creator_id:
            add_message(creator_id, "ai", llm_output.output_text, "address_run")

        return {"settings": state["settings"]}
