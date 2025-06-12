from registry import get_component
from utils.tooling import enable_tool_calling

def load_from_config(cfg):
    llm = get_component("llm", cfg["llm"])
    tools = {name: get_component("tool", name) for name in cfg.get("tools", [])}

    # Separate known fields from config-driven parameters
    known_keys = {"type", "llm", "tools"}
    agent_params = {k: v for k, v in cfg.items() if k not in known_keys}

    @enable_tool_calling(llm, tools, **agent_params)
    def base_agent(state):
        content = state.get("tooling_output", "[No content generated]")
        state["content"] = content
        return state

    return base_agent
