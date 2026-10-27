# Main entry point: one command for every phase.
#   python rag.py build | ask "..." | chat | serve | eval
# Thin front door only; the steps live in ingest/, retrieval/, engines/, and evaluation/.
import argparse
import sys

NOT_BUILT = {"serve": "S16 (web interfaces)", "eval": "S13 (evaluation)"}


def _print_answer(result) -> None:
    print(f"\n{result.answer}\n")
    for s in result.sources:
        print(f"  [Source {s['n']}] {s['source']}, p. {s['page']}")
    print()


def cmd_build(args) -> int:
    from ingest.pipeline import build_index

    stats = build_index(args.use_case)
    print(f"Indexed {stats['files']} files, {stats['pages']} pages, {stats['chunks']} chunks -> {stats['index']}")
    return 0


def cmd_ask(args) -> int:
    from engines.base import get_engine

    _print_answer(get_engine(args.engine, case=args.use_case).answer(args.question))
    return 0


def cmd_chat(args) -> int:
    from engines.base import get_engine

    engine = get_engine(args.engine, case=args.use_case)  # load the index once for the whole session
    print("Ask about the vendor documents. Type q to quit.")
    while (question := input("\n> ").strip()).lower() not in {"q", "quit", "exit"}:
        if question:
            _print_answer(engine.answer(question))
    return 0


def main(argv: list[str] | None = None) -> int:
    from core.config import load_env

    parser = argparse.ArgumentParser(prog="rag.py", description="Enterprise RAG: build the index, then ask.")
    parser.add_argument("--use-case", default=None, help="data/<use-case>/ to use (default: USE_CASE or vendor-risk-compliance)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="Phase 1: load, chunk, embed, and index the source PDFs")
    ask = sub.add_parser("ask", help="Answer one question with citations")
    ask.add_argument("question")
    chat = sub.add_parser("chat", help="Ask questions in a loop")
    for p in (ask, chat):
        p.add_argument("--engine", default="plain_rag")
    for name in NOT_BUILT:
        sub.add_parser(name, help=f"Not built yet: {NOT_BUILT[name]}")
    args = parser.parse_args(argv)

    if args.command in NOT_BUILT:
        print(f"`{args.command}` arrives with {NOT_BUILT[args.command]}.")
        return 1
    load_env()
    try:
        return {"build": cmd_build, "ask": cmd_ask, "chat": cmd_chat}[args.command](args)
    except (RuntimeError, FileNotFoundError, ValueError) as err:
        # Setup problems (no API key, no index, no PDFs) get one clear line instead of a traceback
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
