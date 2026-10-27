# S6/F2: LLM and embeddings provider selection (OpenAI or Azure), shared by S6, S8, S12, S13.
# Same rule as restaurant-ai-platform's core/llm.py (OpenAI key first, then Azure), but models and
# Azure settings come from env vars instead of being hard-coded.
import os

from core.config import DEFAULT_EMBEDDINGS_MODEL, DEFAULT_LLM_MODEL

AZURE_API_VERSION = "2024-10-21"


def provider() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("AZURE_OPENAI_API_KEY"):
        return "azure"
    raise RuntimeError("Set OPENAI_API_KEY (or AZURE_OPENAI_API_KEY) in the .env file at the repo root")


def build_embeddings():
    # S6: lazy import so tests and `rag.py --help` don't pay for langchain_openai
    model = os.environ.get("EMBEDDINGS_MODEL", DEFAULT_EMBEDDINGS_MODEL)
    if provider() == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=model)
    from langchain_openai import AzureOpenAIEmbeddings

    return AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", AZURE_API_VERSION),
        deployment=os.environ.get("AZURE_EMBEDDINGS_DEPLOYMENT", model),
    )


def build_llm():
    # S12: temperature 0 so the same question over the same context gives the same answer
    model = os.environ.get("LLM_MODEL", DEFAULT_LLM_MODEL)
    if provider() == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=0)
    from langchain_openai import AzureChatOpenAI

    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", AZURE_API_VERSION),
        deployment_name=os.environ.get("AZURE_LLM_DEPLOYMENT", model),
        temperature=0,
    )
