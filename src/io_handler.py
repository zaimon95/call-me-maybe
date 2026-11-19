"""Every file access of the project lives here.

Loading: missing file -> unreadable -> invalid JSON -> wrong shape.
Each case is converted into a custom exception from errors.py.
"""

from pathlib import Path
from typing import Any

from src.models import FunctionCall, FunctionDefinition, TestPrompt


def _read_json(path: Path) -> Any:
    """Read and parse a JSON file.

    Raises:
        InputFileError: missing file, permission error, invalid JSON.

    TODO: open with a context manager, json.load, and translate
    FileNotFoundError / PermissionError / json.JSONDecodeError
    (and IsADirectoryError, UnicodeDecodeError...) into InputFileError
    with a message that names the file.
    """
    raise NotImplementedError


def load_functions(path: Path) -> list[FunctionDefinition]:
    """Load and validate functions_definition.json.

    Raises:
        InputFileError: see _read_json.
        SchemaError: not a list, or an entry fails pydantic validation,
            or the list is empty / has duplicate names.

    TODO: _read_json, check it is a list, validate each entry,
    convert pydantic.ValidationError into SchemaError.
    """
    raise NotImplementedError


def load_prompts(path: Path) -> list[TestPrompt]:
    """Load and validate function_calling_tests.json.

    TODO: same pattern as load_functions.
    """
    raise NotImplementedError


def write_results(path: Path, results: list[FunctionCall]) -> None:
    """Write all results as one JSON array.

    Raises:
        OutputFileError: the directory cannot be created or the file
            cannot be written.

    TODO: create the parent directory, dump each result
    (model_dump), write with a context manager.
    """
    raise NotImplementedError
