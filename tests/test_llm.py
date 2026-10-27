# S6/F2: provider selection tests. Constructing the clients makes no network call.
import pytest

from core import llm


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for name in ("OPENAI_API_KEY", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "LLM_MODEL", "EMBEDDINGS_MODEL"):
        monkeypatch.delenv(name, raising=False)


def test_no_key_raises_clear_error() -> None:
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        llm.provider()


def test_openai_key_wins_and_models_come_from_env(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "az-test")
    monkeypatch.setenv("LLM_MODEL", "gpt-test")

    assert llm.provider() == "openai"
    assert type(llm.build_llm()).__name__ == "ChatOpenAI"
    assert llm.build_llm().model_name == "gpt-test"
    assert llm.build_embeddings().model == "text-embedding-3-small"


def test_azure_used_when_only_azure_key_set(monkeypatch) -> None:
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "az-test")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")

    assert llm.provider() == "azure"
    assert type(llm.build_llm()).__name__ == "AzureChatOpenAI"
    assert type(llm.build_embeddings()).__name__ == "AzureOpenAIEmbeddings"
