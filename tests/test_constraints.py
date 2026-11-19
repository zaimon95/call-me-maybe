"""Tests for constraints, WITHOUT the model.

Tip: build a tiny fake Vocabulary (10-20 tokens) so tests are instant
and you can check exactly which tokens are allowed at each state.

TODO:
- ChoiceConstraint: prefixes, options that prefix each other
- NumberConstraint: "-", "3.", "1e5", rejects "1.2.3", "--1"
- StringConstraint: escapes, closing quote, special characters
"""
