"""Pydantic data contracts for inputs and outputs.

Validation happens here, at the boundary: once a model is built, the
rest of the code can trust its content.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

# Types allowed in functions_definition.json. Every value listed here
# must have a branch in FunctionCaller._constraint_for.
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

    Extra keys are forbidden: the subject requires exactly these three
    keys in every output object. Input models keep pydantic's default
    (extra keys ignored) so a definitions file with additional fields
    is still accepted.
    """

    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, Any]
