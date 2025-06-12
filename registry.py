from config_loader import CONFIG
from importlib import import_module


def get_graph(name: str):
    module = import_module(f"graphs.{name}")
    if not hasattr(module, "build_graph"):
        raise ValueError(f"Graph module 'graphs.{name}' missing 'build_graph'")
    return module.build_graph()


def get_agent(name: str):
    cfg = CONFIG.get("agents", {}).get(name)
    if not cfg:
        raise ValueError(f"Agent '{name}' not found in config.yaml")

    module = import_module(f"agents.{cfg['type']}")
    return module.load_from_config(cfg)


def get_llm(name: str):
    cfg = CONFIG.get("llms", {}).get(name)
    if not cfg:
        raise ValueError(f"LLM '{name}' not found in config.yaml")

    module = import_module(f"llms.{cfg['type']}")
    llm = module.load_from_config(cfg)
    if not hasattr(llm, "invoke"):
        raise TypeError(f"LLM '{name}' must implement .invoke()")
    return llm


def get_tool(name: str):
    cfg = CONFIG.get("tools", {}).get(name)
    if not cfg:
        raise ValueError(f"Tool '{name}' not found in config.yaml")

    module = import_module(f"tools.{cfg['type']}")
    tool = module.load_from_config(cfg)
    if not callable(tool):
        raise TypeError(f"Tool '{name}' must be callable")
    return tool


def get_component(kind: str, name: str):
    if kind == "agent":
        return get_agent(name)
    elif kind == "tool":
        return get_tool(name)
    elif kind == "llm":
        return get_llm(name)
    elif kind == "graph":
        return get_graph(name)
    else:
        raise ValueError(f"Unknown component kind: {kind}")
