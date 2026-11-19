"""Custom exception hierarchy.

Every expected failure (bad file, bad JSON, model error...) is turned
into one of these exceptions, so __main__ only needs one except clause
to print a clean message instead of a traceback.
"""


class CallMeMaybeError(Exception):
    """Base class for every error raised by this project."""


class InputFileError(CallMeMaybeError):
    """An input file is missing, unreadable or not valid JSON."""


class SchemaError(CallMeMaybeError):
    """An input file is valid JSON but does not have the expected shape."""


class ModelError(CallMeMaybeError):
    """The LLM could not be loaded or failed during generation."""


class GenerationError(CallMeMaybeError):
    """Constrained decoding could not produce a value (e.g. max length)."""


class OutputFileError(CallMeMaybeError):
    """The output file could not be written."""
