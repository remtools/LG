from registry import get_component
from utils.tooling import enable_tool_calling

def load_from_config(cfg):
    llm = get_component("llm", cfg["llm"])
    tools = {name: get_component("tool", name) for name in cfg.get("tools", [])}

    def base_agent(state):
        input_text = state.get("input", "")
        response = llm.invoke(input_text)
        return {"output": getattr(response, "content", "[NO RESPONSE]")}

    if tools:
        return enable_tool_calling(base_agent, llm, tools)

    return base_agent
