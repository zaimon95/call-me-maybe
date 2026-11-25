"""Every file access of the project lives here.

Loading: missing file -> unreadable -> invalid JSON -> wrong shape.
Each case is converted into a custom exception from errors.py.
"""

import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from src.errors import InputFileError, OutputFileError, SchemaError
from src.models import FunctionCall, FunctionDefinition, TestPrompt

Model = TypeVar("Model", bound=BaseModel)


def _read_json(path: Path) -> Any:
    """Read and parse a JSON file.

    Raises:
        InputFileError: missing file, permission error, invalid JSON.
    """
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise InputFileError(f"{path}: file not found") from error
    except IsADirectoryError as error:
        raise InputFileError(f"{path}: is a directory") from error
    except PermissionError as error:
        raise InputFileError(f"{path}: permission denied") from error
    except OSError as error:
        raise InputFileError(f"{path}: cannot read file: {error}") from error
    except UnicodeDecodeError as error:
        raise InputFileError(f"{path}: not valid UTF-8 text") from error
    except json.JSONDecodeError as error:
        raise InputFileError(
            f"{path}: invalid JSON at line {error.lineno}, "
            f"column {error.colno}: {error.msg}") from error


def _read_list(path: Path) -> list[Any]:
    """Read a JSON file whose top level must be an array.

    Raises:
        InputFileError: see _read_json.
        SchemaError: the top level is not a list.
    """
    data = _read_json(path)
    if not isinstance(data, list):
        raise SchemaError(
            f"{path}: expected a JSON list, got {type(data).__name__}")
    return data


def _validate_entries(
    path: Path,
    entries: list[Any],
    model: type[Model],
) -> list[Model]:
    """Validate every entry with a pydantic model.

    Raises:
        SchemaError: names the first invalid entry and the reason.
    """
    validated: list[Model] = []
    for index, entry in enumerate(entries):
        try:
            validated.append(model.model_validate(entry))
        except ValidationError as error:
            reasons = "; ".join(
                f"{'.'.join(str(loc) for loc in detail['loc'])}: "
                f"{detail['msg']}"
                for detail in error.errors())
            raise SchemaError(
                f"{path}: entry {index} is invalid ({reasons})") from error
    return validated


def load_functions(path: Path) -> list[FunctionDefinition]:
    """Load and validate functions_definition.json.

    Raises:
        InputFileError: see _read_json.
        SchemaError: not a list, or an entry fails pydantic validation,
            or the list is empty / has duplicate names.
    """
    entries = _read_list(path)
    if not entries:
        raise SchemaError(f"{path}: no function defined")
    functions = _validate_entries(path, entries, FunctionDefinition)
    seen: set[str] = set()
    for function in functions:
        if function.name in seen:
            raise SchemaError(
                f"{path}: function {function.name!r} defined twice")
        seen.add(function.name)
    return functions


def load_prompts(path: Path) -> list[TestPrompt]:
    """Load and validate function_calling_tests.json.

    Raises:
        InputFileError: see _read_json.
        SchemaError: not a list, or an entry fails pydantic validation.
    """
    return _validate_entries(path, _read_list(path), TestPrompt)


def write_results(path: Path, results: list[FunctionCall]) -> None:
    """Write all results as one JSON array.

    Raises:
        OutputFileError: the directory cannot be created or the file
            cannot be written.
    """
    content = [result.model_dump() for result in results]
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except OSError as error:
        raise OutputFileError(
            f"{path}: cannot write file: {error}") from error
