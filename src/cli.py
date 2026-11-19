"""Command-line argument parsing."""

import argparse
from pathlib import Path

DEFAULT_FUNCTIONS = Path("data/input/functions_definition.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calls.json")


class Arguments(argparse.Namespace):
    """Typed view of the parsed arguments (helps mypy)."""

    functions_definition: Path
    input: Path
    output: Path


def parse_args(argv: list[str] | None = None) -> Arguments:
    """Parse the command line.

    Args:
        argv: Arguments to parse; None means sys.argv[1:].

    Returns:
        The parsed arguments, with default paths filled in.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition", type=Path, default=DEFAULT_FUNCTIONS)
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv, namespace=Arguments())
