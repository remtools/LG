from langgraph.graph import StateGraph, END
from registry import get_component
import yaml


from langgraph.graph import StateGraph, END
from registry import get_component
import config_loader  # or wherever your config is loaded from

def build_graph(cfg=None):
    # Load full config if not passed in

    cfg = cfg or yaml.safe_load(open("config.yaml"))

    graph_cfg = cfg["graphs"]["main_flow"]
    agent_names = list(cfg["agents"].keys())

    agents = {name: get_component("agent", name) for name in agent_names}

    builder = StateGraph(dict)

    # Add nodes dynamically
    for name in agent_names:
        builder.add_node(name, agents[name])

    # Static edges (for now) — or make this dynamic later
    builder.set_entry_point(graph_cfg.get("entry", "researcher"))
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", END)

    return builder.compile()
