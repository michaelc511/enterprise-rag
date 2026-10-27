# S12: plain RAG engine: retrieve -> assemble context -> grounded, cited answer.
from engines.base import Answer, BaseEngine
from retrieval import context as ctx
from retrieval.search import TOP_K, search

NOT_FOUND = "I cannot find the answer in the provided documents."
DISCLAIMER = "Not legal advice."

# S12: the PDF's prompt plus three fixes: an exact refusal string, mandatory [Source n] citations,
# and the "Not legal advice" disclaimer the use case requires on every answer
SYSTEM_PROMPT = (
    "You are OpsVault's vendor risk and compliance assistant. Answer the question using ONLY the "
    "context below. Cite every fact with its source number, like [Source 1]. If the context does not "
    f"contain the answer, reply exactly: \"{NOT_FOUND}\" Do not use outside knowledge. "
    f"End every answer with: \"{DISCLAIMER}\""
)


class PlainRagEngine(BaseEngine):
    name = "plain_rag"

    def __init__(self, index, llm, k: int = TOP_K) -> None:
        self.index = index
        self.llm = llm
        self.k = k

    @classmethod
    def from_config(cls, case: str | None = None, k: int = TOP_K) -> "PlainRagEngine":
        from core import config
        from core.llm import build_embeddings, build_llm
        from ingest.vectorstore import load_index

        # F3: load the cached index instead of re-embedding the corpus on every question
        index = load_index(build_embeddings(), config.index_dir(case))
        return cls(index, build_llm(), k)

    def answer(self, question: str) -> Answer:
        from langchain_core.prompts import ChatPromptTemplate

        docs = search(self.index, question, self.k)  # S7
        if not docs:
            # S12: nothing retrieved means nothing to ground on, so skip the LLM call entirely
            return Answer(question, f"{NOT_FOUND} {DISCLAIMER}", [], self.name)
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ])
        reply = (prompt | self.llm).invoke({"context": ctx.assemble_context(docs), "question": question})  # S11
        text = getattr(reply, "content", str(reply)).strip()
        return Answer(question, text, ctx.sources(docs), self.name)
