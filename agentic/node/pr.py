from openai import OpenAI
from dotenv import load_dotenv
import inspect
from agentic.state import State
from prompt.pr_prompt import PR_Prompt
load_dotenv()           
client = OpenAI()

class PR_Nodes:

    def greet_run(state: State):
        llm_output = client.responses.create(
            model = "gpt-4.1", 
            input = state["settings"]["creator_latest_response"], 
            previous_response_id = state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.NODE1_PROMPT
        )
        #需要变成function
        if "[" in llm_output.output_text and "]" in llm_output.output_text and "结束" in llm_output.output_text:
            state["settings"]["node_change"] = True
            return {}

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id

        print("\n" + llm_output.output_text)
        return {}
    
    def type_run(state: State):
        llm_output = client.responses.create(
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
            state["settings"]["node_change"] = True
            return {}

        #改逻辑
        state["settings"]["openai_previous_id"]= llm_output.id

        print("\n" + llm_output.output_text)
        return {}


