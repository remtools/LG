
from registry import get_component
from utils.tooling import enable_tool_calling

def load_from_config(cfg):
    llm = get_component("llm", cfg["llm"])
    tools = {name: get_component("tool", name) for name in cfg.get("tools", [])}

    @enable_tool_calling(llm, tools)
    def base_agent(state):
        content = state.get("tooling_output", "[NO TOOLING OUTPUT]")
        state["content"] = content
        return state

    return base_agent
