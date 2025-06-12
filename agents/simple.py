from registry import get_component
from utils.tooling import enable_tool_calling

def load_from_config(cfg):
    # Load LLM
    llm = get_component("llm", cfg["llm"])

    # Load tools if defined
    tools = {
        name: get_component("tool", name)
        for name in cfg.get("tools", [])
    }

    # Separate out known config keys to leave room for agent customization
    known_keys = {"type", "llm", "tools"}
    agent_params = {
        k: v for k, v in cfg.items() if k not in known_keys
    }

    # If tools are present, wrap with tool-calling logic
    if tools:
        @enable_tool_calling(llm, tools, **agent_params)
        def base_agent(state):
            content = state.get("tooling_output", "[No content generated]")
            state["content"] = content
            return state
    else:
        # No tools — directly call LLM with a prompt
        def base_agent(state):
            input_text = state.get("input", "")
            prompt = agent_params.get("system_prompt", "You are a helpful assistant.") + f"\nUser: {input_text}\nAssistant:"
            response = llm.invoke(prompt)
            state["content"] = getattr(response, "content", "[No content]")
            return state

    return base_agent
