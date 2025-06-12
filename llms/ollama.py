from langchain_community.chat_models import ChatOllama

def load_from_config(cfg):
    """
    Load an Ollama-compatible LLM using LangChain's ChatOllama wrapper.

    Expects `cfg` to contain:
        - model: Name of the local Ollama model (e.g. "llama2", "gemma:7b")
        - temperature: (optional) Decoding temperature

    Returns:
        An instance of ChatOllama ready for use in LangChain or LangGraph.
    """
    return ChatOllama(
        model=cfg["model"],
        temperature=cfg.get("temperature", 0.7)
    )
