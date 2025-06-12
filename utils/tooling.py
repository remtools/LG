import re

def enable_tool_calling(agent_func, llm, tools, max_steps=4):
    """
    Wraps a base agent function with tool-calling logic.

    - Injects available tools into prompt
    - Intercepts `Calling: tool_name("arg")` from LLM
    - Executes tool and loops prompt with tool result
    - Falls back to original agent if no tool call is found
    """

    def wrapped(state):
        input_text = state.get("input", "")
        if not input_text:
            return {"output": "[NO INPUT PROVIDED]"}

        # Tool descriptions from docstrings
        tool_descriptions = "\n".join([
            f"- {name}(...)  # {tool.__doc__ or 'No description'}"
            for name, tool in tools.items()
        ])
        
        first_tool = list(tools.keys())[0] if tools else "tool_name"

        # System prompt with embedded tool docs
        system_prompt = f"""You are an assistant that must use tools to answer questions when applicable.
Never guess. If a tool is available, use it.
Call a tool like this (with no extra commentary):
Calling: {first_tool}("argument")

Available tools:
{tool_descriptions}
"""

        # Initialize prompt history
        history = f"{system_prompt}\nUser: {input_text}\nAssistant:"

        for step in range(max_steps):
            print(f"\n🔁 Step {step+1}")
            response = llm.invoke(history)
            content = getattr(response, "content", "").strip()
            print("🤖 LLM says:\n", content)

            # Check for tool call
            match = re.search(r"Calling:\s*(\w+)\((.*?)\)\s*$", content, re.DOTALL)
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

                    # Append tool result to history and re-prompt
                    history += f"\nAssistant: Calling: {tool_name}({raw_arg})"
                    history += f"\n[Tool output]: {result}"
                    history += f"\nUser: Now, based on the tool result above, please complete the task: {input_text}\nAssistant:"
                except Exception as e:
                    print("❌ Tool execution error:", e)
                    history += f"\nAssistant: [ERROR running {tool_name}]: {e}"
            else:
                return {"output": content}

        return {"output": "[Agent stopped after max steps]"}

    return wrapped
