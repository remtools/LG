### researcher.py

from registry import get_component
from utils.tooling import enable_tool_calling

def load_from_config(cfg):
    llm = get_component("llm", cfg["llm"])
    tools = {name: get_component("tool", name) for name in cfg.get("tools", [])}

    def base_agent(state):
        input_text = state.get("input", "")
        prompt = (
            f"You are a researcher who is an expert at getting info from the internet.\n\n"
            f"Get content for below:\n\n"
            f"{input_text}"
        )
        response = llm.invoke(prompt)
        output = getattr(response, "content", "[NO RESPONSE]")
        state["research"] = output
        state["output"] = output
        return state

    agent = enable_tool_calling(base_agent, llm, tools) if tools else base_agent
    return agent
