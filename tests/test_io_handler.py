"""Tests for input loading: write these BEFORE implementing io_handler.

TODO, one test per case (use pytest's tmp_path fixture):
- missing file            -> InputFileError
- invalid JSON            -> InputFileError
- JSON object, not a list -> SchemaError
- entry missing "name"    -> SchemaError
- unknown parameter type  -> SchemaError
- valid file              -> list of FunctionDefinition
"""
