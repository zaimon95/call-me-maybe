"""Tests for input/output files (src/io_handler.py).

No model is loaded here: every test runs in a few milliseconds.
Run with: uv run pytest
"""

import json
from pathlib import Path
from typing import Any

import pytest

from src.errors import InputFileError, OutputFileError, SchemaError
from src.io_handler import load_functions, load_prompts, write_results
from src.models import FunctionCall

VALID_FUNCTION: dict[str, Any] = {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
    "returns": {"type": "number"},
}


def write_json(path: Path, content: Any) -> Path:
    """Write any Python value as JSON into path and return the path."""
    path.write_text(json.dumps(content), encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# load_functions: file-level errors -> InputFileError
# --------------------------------------------------------------------------

def test_functions_missing_file(tmp_path: Path) -> None:
    """A path that does not exist is an input error, not a crash."""
    with pytest.raises(InputFileError):
        load_functions(tmp_path / "nope.json")


def test_functions_path_is_directory(tmp_path: Path) -> None:
    """Opening a directory raises IsADirectoryError: must be converted."""
    with pytest.raises(InputFileError):
        load_functions(tmp_path)


def test_functions_invalid_json(tmp_path: Path) -> None:
    """Broken JSON syntax (here a trailing comma) is an input error."""
    path = tmp_path / "broken.json"
    path.write_text('[{"name": "fn",}]', encoding="utf-8")
    with pytest.raises(InputFileError):
        load_functions(path)


def test_functions_empty_file(tmp_path: Path) -> None:
    """An empty file is not valid JSON either."""
    path = tmp_path / "empty.json"
    path.write_text("", encoding="utf-8")
    with pytest.raises(InputFileError):
        load_functions(path)


# --------------------------------------------------------------------------
# load_functions: valid JSON, wrong shape -> SchemaError
# --------------------------------------------------------------------------

def test_functions_object_instead_of_list(tmp_path: Path) -> None:
    """The top level must be a list of definitions."""
    path = write_json(tmp_path / "f.json", VALID_FUNCTION)
    with pytest.raises(SchemaError):
        load_functions(path)


def test_functions_empty_list(tmp_path: Path) -> None:
    """No function at all: the model would have nothing to choose."""
    path = write_json(tmp_path / "f.json", [])
    with pytest.raises(SchemaError):
        load_functions(path)


def test_functions_missing_name(tmp_path: Path) -> None:
    """A required field is missing: pydantic error -> SchemaError."""
    entry = {k: v for k, v in VALID_FUNCTION.items() if k != "name"}
    path = write_json(tmp_path / "f.json", [entry])
    with pytest.raises(SchemaError):
        load_functions(path)


def test_functions_unknown_parameter_type(tmp_path: Path) -> None:
    """A type that has no constraint must be rejected at load time."""
    entry = dict(VALID_FUNCTION, parameters={"a": {"type": "complex"}})
    path = write_json(tmp_path / "f.json", [entry])
    with pytest.raises(SchemaError):
        load_functions(path)


def test_functions_duplicate_names(tmp_path: Path) -> None:
    """Two functions with the same name make the choice ambiguous."""
    path = write_json(tmp_path / "f.json", [VALID_FUNCTION, VALID_FUNCTION])
    with pytest.raises(SchemaError):
        load_functions(path)


# --------------------------------------------------------------------------
# load_functions: valid inputs
# --------------------------------------------------------------------------

def test_functions_valid(tmp_path: Path) -> None:
    """A correct file gives validated FunctionDefinition objects."""
    path = write_json(tmp_path / "f.json", [VALID_FUNCTION])
    functions = load_functions(path)
    assert len(functions) == 1
    assert functions[0].name == "fn_add_numbers"
    assert list(functions[0].parameters) == ["a", "b"]
    assert functions[0].parameters["a"].type == "number"


def test_functions_extra_keys_ignored(tmp_path: Path) -> None:
    """Unknown fields in the INPUT are tolerated (see models.py)."""
    entry = dict(VALID_FUNCTION, author="someone")
    path = write_json(tmp_path / "f.json", [entry])
    assert load_functions(path)[0].name == "fn_add_numbers"


# --------------------------------------------------------------------------
# load_prompts
# --------------------------------------------------------------------------

def test_prompts_valid(tmp_path: Path) -> None:
    """Order is kept: output entries must follow the input order."""
    content = [{"prompt": "What is 2 + 3?"}, {"prompt": "Reverse 'hi'"}]
    path = write_json(tmp_path / "p.json", content)
    prompts = load_prompts(path)
    assert [p.prompt for p in prompts] == ["What is 2 + 3?", "Reverse 'hi'"]


def test_prompts_special_characters(tmp_path: Path) -> None:
    """Quotes, backslashes and accents survive the round trip."""
    text = 'Say "bonjour" \\ à Zoé'
    path = write_json(tmp_path / "p.json", [{"prompt": text}])
    assert load_prompts(path)[0].prompt == text


def test_prompts_missing_file(tmp_path: Path) -> None:
    """Same file errors as for the definitions."""
    with pytest.raises(InputFileError):
        load_prompts(tmp_path / "nope.json")


def test_prompts_not_a_list(tmp_path: Path) -> None:
    """The top level must be a list."""
    path = write_json(tmp_path / "p.json", {"prompt": "hello"})
    with pytest.raises(SchemaError):
        load_prompts(path)


def test_prompts_wrong_key(tmp_path: Path) -> None:
    """Each entry needs a "prompt" field."""
    path = write_json(tmp_path / "p.json", [{"question": "hello"}])
    with pytest.raises(SchemaError):
        load_prompts(path)


def test_prompts_wrong_value_type(tmp_path: Path) -> None:
    """The prompt must be a string, not a number."""
    path = write_json(tmp_path / "p.json", [{"prompt": 42}])
    with pytest.raises(SchemaError):
        load_prompts(path)


# --------------------------------------------------------------------------
# write_results
# --------------------------------------------------------------------------

def test_write_creates_directory_and_valid_json(tmp_path: Path) -> None:
    """Missing parent folders are created; the file is a JSON array."""
    output = tmp_path / "data" / "output" / "function_calls.json"
    call = FunctionCall(
        prompt="What is 2 + 3?",
        name="fn_add_numbers",
        parameters={"a": 2.0, "b": 3.0},
    )
    write_results(output, [call])
    content = json.loads(output.read_text(encoding="utf-8"))
    assert content == [{
        "prompt": "What is 2 + 3?",
        "name": "fn_add_numbers",
        "parameters": {"a": 2.0, "b": 3.0},
    }]


def test_write_empty_list(tmp_path: Path) -> None:
    """No result at all still produces a valid (empty) JSON array."""
    output = tmp_path / "out.json"
    write_results(output, [])
    assert json.loads(output.read_text(encoding="utf-8")) == []


def test_write_parent_is_a_file(tmp_path: Path) -> None:
    """The parent "directory" is a regular file: cannot write there."""
    blocker = tmp_path / "blocker"
    blocker.write_text("", encoding="utf-8")
    with pytest.raises(OutputFileError):
        write_results(blocker / "out.json", [])
