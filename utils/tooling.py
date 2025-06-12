import re

def enable_tool_calling(llm, tools, system_prompt=None, max_steps=4, **kwargs):
    def decorator(agent_func):
        def wrapped(state):
            input_text = state.get("input", "")
            if not input_text:
                state["output"] = "[NO INPUT PROVIDED]"
                return state

            # Generate tool descriptions
            tool_descriptions = "\n".join([
                f"- {name}(...)  # {tool.__doc__ or 'No description'}"
                for name, tool in tools.items()
            ])
            first_tool = list(tools.keys())[0] if tools else "tool_name"

            # Compose dynamic prompt
            default_prompt = "You are an assistant."
            core_prompt = system_prompt or default_prompt
            core_prompt += f"\n\nUse tools only when needed.\nAvailable tools:\n{tool_descriptions}"

            history = f"{core_prompt}\nUser: {input_text}\nAssistant:"

            for step in range(max_steps):
                print(f"\n🔁 Step {step + 1}")
                response = llm.invoke(history)
                content = getattr(response, "content", "").strip()
                print("🤖 LLM says:\n", content)

                # Detect tool call
                match = re.search(r"(?:Calling:\s*)?(\w+)\((.*?)\)", content)

                if match:
                    tool_name, raw_arg = match.groups()
                    tool = tools.get(tool_name)

                    if not tool:
                        print(f"❌ Unknown tool: {tool_name}")
                        history += f"\nAssistant: [ERROR: Unknown tool '{tool_name}']"
                        continue

                    try:
                        if "=" in raw_arg:
                            kwargs = eval(f"dict({raw_arg})")
                            print("🧪 Tool kwargs:", kwargs)
                            result = tool(**kwargs)
                        else:
                            arg = eval(raw_arg)
                            print("🧪 Tool arg:", arg)
                            result = tool(arg)

                        print(f"🔧 Tool call: {tool_name}({raw_arg}) → {result}")
                        history += f"\nAssistant: Calling: {tool_name}({raw_arg})"
                        history += f"\n[Tool output]: {result}"
                        history += f"\nUser: Based on the tool result above, complete the task.\nAssistant:"
                        continue

                    except Exception as e:
                        print(f"❌ Tool execution error: {e}")
                        history += f"\nAssistant: [ERROR running {tool_name}]: {e}"
                        continue

                # If no tool call, return result
                state["tooling_output"] = content
                return agent_func(state)

            state["tooling_output"] = "[Agent stopped after max steps]"
            return agent_func(state)

        return wrapped
    return decorator
