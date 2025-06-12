from langchain_community.chat_models import ChatOpenAI
def load_from_config(cfg):
    return ChatOpenAI(model_name=cfg["model"], temperature=cfg.get("temperature", 0.7))
