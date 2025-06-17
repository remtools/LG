### test_graph.py

from registry import get_component

# Load the LangGraph pipeline
graph = get_component("graph", "main_flow")

# Provide initial state
initial_state = {"input": "cehck the date and whats the news today?"}

print("Sending initial state:", initial_state)

# Run the graph
final_state = graph.invoke(initial_state)

print(final_state['content'])