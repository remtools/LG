### test_graph.py

from registry import get_component

# Load the LangGraph pipeline
graph = get_component("graph", "main_flow")

# Provide initial state
initial_state = {"input": "bbands in goa"}

print("Sending initial state:", initial_state)

# Run the graph
final_state = graph.invoke(initial_state)

# Print out all state keys
print("\nFinal state:")
for k, v in final_state.items():
    print(f"{k}: {v}\n")
