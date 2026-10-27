# S12: plain RAG engine tests with a fake index and a fake LLM that records its input.
import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from engines import base
from engines.plain_rag_engine import DISCLAIMER, NOT_FOUND, PlainRagEngine


class FakeIndex:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search(self, question, k):
        return self.docs[:k]


def recording_llm(reply: str, seen: list):
    def _call(prompt_value):
        seen.append(prompt_value.to_messages())
        return AIMessage(content=reply)

    return RunnableLambda(_call)


def test_answer_grounds_prompt_in_numbered_context_and_returns_sources() -> None:
    docs = [Document(page_content="Notify within 48 hours.", metadata={"source": "msa/s.pdf", "page": 3})]
    seen = []
    engine = PlainRagEngine(FakeIndex(docs), recording_llm(f"48 hours [Source 1]. {DISCLAIMER}", seen))

    result = engine.answer("What is the breach notice window?")

    system, human = seen[0]
    assert NOT_FOUND in system.content and DISCLAIMER in system.content
    assert "[Source 1: s.pdf, p. 3]\nNotify within 48 hours." in human.content
    assert "What is the breach notice window?" in human.content
    assert result.answer == f"48 hours [Source 1]. {DISCLAIMER}"
    assert result.sources == [{"n": 1, "source": "msa/s.pdf", "page": 3}]
    assert result.engine == "plain_rag"


def test_no_retrieved_docs_skips_llm_and_refuses() -> None:
    seen = []
    result = PlainRagEngine(FakeIndex([]), recording_llm("should not be called", seen)).answer("anything")
    assert seen == []
    assert result.answer == f"{NOT_FOUND} {DISCLAIMER}"


def test_get_engine_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="plain_rag"):
        base.get_engine("nope")
