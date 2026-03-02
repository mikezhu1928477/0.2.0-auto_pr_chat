from openai import OpenAI
from dotenv import load_dotenv
import inspect
from agentic.state import State
from prompt.pr_prompt import PR_Prompt
load_dotenv()           
client = OpenAI()

class PR_Nodes:
    @staticmethod
    def _check_end(llm_output_text: str) -> bool:
        return "[" in llm_output_text and "]" in llm_output_text and "结束" in llm_output_text

    @staticmethod
    def _update_settings(state: State, llm_output) -> None:
        state["settings"]["openai_previous_id"] = llm_output.id
        state["settings"]["llm_latest_response"] = llm_output.output_text

    @staticmethod
    def _end_node(state: State) -> None:
        state["settings"]["node_change"] = True

    # ──────────────────────────────────────────────────────────────────

    def greet_run(state: State):
        llm_output = client.responses.create(
            model="gpt-4.1",
            input=state["settings"]["creator_latest_response"],
            previous_response_id=state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.GREET_PROMPT
        )
        if PR_Nodes._check_end(llm_output.output_text):
            PR_Nodes._end_node(state)
            return {}
        PR_Nodes._update_settings(state, llm_output)
        print("\n" + llm_output.output_text)
        return {}


    def type_run(state: State):
        llm_output = client.responses.create(
            model="gpt-4.1",
            input=state["settings"]["creator_latest_response"],
            previous_response_id=state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.TYPE_PROMPT.format(
                price=state["task"]["ai_expected"]["maximum_price"],
                collab_type=state["task"]["ai_expected"]["collab_type"],
                delivery_type=state["task"]["ai_expected"]["delivery_type"]
            )
        )
        if PR_Nodes._check_end(llm_output.output_text):
            PR_Nodes._end_node(state)
            return {}
        PR_Nodes._update_settings(state, llm_output)
        print("\n" + llm_output.output_text)
        return {}


    def schedule_run(state: State):
        llm_output = client.responses.create(
            model="gpt-4.1",
            input=state["settings"]["creator_latest_response"],
            previous_response_id=state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.SCHEDULE_PROMPT.format(
                schedule=state["task"]["ai_expected"]["schedule"],
            )
        )
        if PR_Nodes._check_end(llm_output.output_text):
            PR_Nodes._end_node(state)
            return {}
        PR_Nodes._update_settings(state, llm_output)
        print("\n" + llm_output.output_text)
        return {}


    def product_run(state: State):
        llm_output = client.responses.create(
            model="gpt-4.1",
            input=state["settings"]["creator_latest_response"],
            previous_response_id=state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.PRODUCT_PROMPT
        )

        if PR_Nodes._check_end(llm_output.output_text):
            PR_Nodes._end_node(state)
            return {}
        PR_Nodes._update_settings(state, llm_output)
        print("\n" + llm_output.output_text)
        return {}


    def address_run(state: State):
        llm_output = client.responses.create(
            model="gpt-4.1",
            input=state["settings"]["creator_latest_response"],
            previous_response_id=state["settings"]["openai_previous_id"],
            instructions=PR_Prompt.ADDRESS_PROMPT
        )
        if PR_Nodes._check_end(llm_output.output_text):
            PR_Nodes._end_node(state)
            return {}
        PR_Nodes._update_settings(state, llm_output)
        print("\n" + llm_output.output_text)
        return {}