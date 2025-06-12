### test_graph.py

from registry import get_component

# Load the LangGraph pipeline
graph = get_component("graph", "main_flow")

# Provide initial state
initial_state = {"input": "Use the web_search tool to look up 'latest news in AI today"}

print("Sending initial state:", initial_state)

# Run the graph
final_state = graph.invoke(initial_state)

print(final_state['content'])