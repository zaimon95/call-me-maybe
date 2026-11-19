"""Entry point: uv run python -m src [options]."""

import sys

from llm_sdk import Small_LLM_Model

from src.cli import Arguments, parse_args
from src.errors import CallMeMaybeError, ModelError
from src.function_caller import FunctionCaller
from src.io_handler import load_functions, load_prompts, write_results
from src.models import FunctionCall, FunctionDefinition, TestPrompt
from src.vocabulary import Vocabulary

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INTERRUPTED = 130


def _log(message: str) -> None:
    """Print a progress or error message on stderr (never on stdout)."""
    print(message, file=sys.stderr)


def _build_caller(functions: list[FunctionDefinition]) -> FunctionCaller:
    """Load the LLM and the vocabulary, then build the FunctionCaller.

    The vocabulary needs the exact number of logits the model returns,
    which is only known after one forward pass: we probe it once here.

    Raises:
        ModelError: the SDK failed (missing weights, out of memory...).
    """
    _log("Loading model...")
    try:
        model = Small_LLM_Model()
        probe_ids = model.encode("probe")[0].tolist()
        vocab_size = len(model.get_logits_from_input_ids(probe_ids))
        vocab_path = model.get_path_to_vocab_file()
    except (OSError, RuntimeError, ValueError) as error:
        raise ModelError(f"cannot load the model: {error}") from error
    vocab = Vocabulary(vocab_path, vocab_size)
    return FunctionCaller(model, vocab, functions)


def _process_all(
    caller: FunctionCaller,
    prompts: list[TestPrompt],
) -> list[FunctionCall]:
    """Run every prompt; a failing prompt is reported and skipped."""
    results: list[FunctionCall] = []
    total = len(prompts)
    for index, test in enumerate(prompts, start=1):
        _log(f"[{index}/{total}] {test.prompt}")
        try:
            results.append(caller.call(test.prompt))
        except CallMeMaybeError as error:
            _log(f"  skipped: {error}")
    return results


def _run(args: Arguments) -> None:
    """Whole pipeline: load inputs, call the model, write the output."""
    functions = load_functions(args.functions_definition)
    prompts = load_prompts(args.input)
    caller = _build_caller(functions)
    results = _process_all(caller, prompts)
    write_results(args.output, results)
    _log(f"{len(results)}/{len(prompts)} calls written to {args.output}")


def main() -> int:
    """Parse arguments, run the pipeline and return the exit status."""
    args = parse_args()
    try:
        _run(args)
    except CallMeMaybeError as error:
        _log(f"Error: {error}")
        return EXIT_ERROR
    except KeyboardInterrupt:
        _log("Interrupted.")
        return EXIT_INTERRUPTED
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
