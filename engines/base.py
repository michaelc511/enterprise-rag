# F12: BaseEngine interface + get_engine() factory, so S17's agent is a second engine, not a rewrite.
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

ENGINES = ("plain_rag",)


@dataclass
class Answer:
    question: str
    answer: str
    sources: list[dict] = field(default_factory=list)
    engine: str = ""


class BaseEngine(ABC):
    name = "base"

    @abstractmethod
    def answer(self, question: str) -> Answer: ...


def get_engine(name: str = "plain_rag", **kwargs) -> BaseEngine:
    # F12: lazy import so loading one engine never pulls in another engine's dependencies
    if name == "plain_rag":
        from engines.plain_rag_engine import PlainRagEngine

        return PlainRagEngine.from_config(**kwargs)
    raise ValueError(f"Unknown engine {name!r}; choose from {', '.join(ENGINES)}")
