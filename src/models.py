"""Pydantic data contracts for inputs and outputs.

Validation happens here, at the boundary: once a model is built, the
rest of the code can trust its content.
"""

from typing import Any, Literal

from pydantic import BaseModel

# Types allowed in functions_definition.json.
# TODO: check which types the subject expects (number, string,
# boolean... maybe integer?) and keep this list in sync with
# the constraints you implement.
ParamType = Literal["number", "string", "boolean"]


class ParameterSpec(BaseModel):
    """Type description of one argument (or of a return value)."""

    type: ParamType


class FunctionDefinition(BaseModel):
    """One callable function, as described in functions_definition.json."""

    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ParameterSpec


class TestPrompt(BaseModel):
    """One entry of function_calling_tests.json."""

    prompt: str


class FunctionCall(BaseModel):
    """One entry of the output file.

    TODO: decide how to forbid extra keys (the subject says
    "no extra keys") - look at pydantic's model configuration.
    """

    prompt: str
    name: str
    parameters: dict[str, Any]
