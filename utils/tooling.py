import re
def enable_tool_calling(llm, tools, system_prompt=None, max_steps=4, **kwargs):
    def decorator(agent_func):
        def wrapped(state):
            input_text = state.get("input", "")
            if not input_text:
                state["output"] = "[NO INPUT PROVIDED]"
                return state

            tool_descriptions = "\n".join([
                f"- {name}(...)  # {tool.__doc__ or 'No description'}"
                for name, tool in tools.items()
            ])
            first_tool = list(tools.keys())[0] if tools else "tool_name"

            # Default prompt template
            default_prompt = f"""You are an assistant. Use tools only when needed.
If confident, respond directly. Otherwise, call a tool like:
Calling: {first_tool}("argument")
"""

            # Append available tools always
            core_prompt = system_prompt or default_prompt
            if "available tools" not in core_prompt.lower():
                core_prompt += f"\n\nAvailable tools:\n{tool_descriptions}"

            history = f"{core_prompt}\nUser: {input_text}\nAssistant:"

            for step in range(max_steps):
                print(f"\n🔁 Step {step+1}")
                response = llm.invoke(history)
                content = getattr(response, "content", "").strip()
                print("🤖 LLM says:\n", content)

                # Tool call detection...
                # (same logic as before)

                # Otherwise, no tool call — return
                state["tooling_output"] = content
                return agent_func(state)

            state["tooling_output"] = "[Agent stopped after max steps]"
            return agent_func(state)

        return wrapped
    return decorator
