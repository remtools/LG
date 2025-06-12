from langgraph.graph import StateGraph, END
from registry import get_component


def build_graph(cfg=None):
    lyrics_finder = get_component("agent", "lyrics_finder")
    writer = get_component("agent", "writer")

    builder = StateGraph(dict)  # Use plain dict to avoid schema issues
    builder.add_node("lyrics_finder", lyrics_finder)
    builder.add_node("writer", writer)
    
    builder.set_entry_point("lyrics_finder")    
    builder.add_edge("lyrics_finder", "writer")
    builder.add_edge("writer", END)

    return builder.compile()
