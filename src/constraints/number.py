"""Generate a JSON number."""

from src.constraints.base import Constraint
from src.vocabulary import BoolMask


class NumberConstraint(Constraint):
    """Allows only text that stays a valid partial JSON number.

    TODO: write down the grammar first ( -? digits (. digits)?
    ([eE] [+-]? digits)? ) and the states it implies. Decide how
    the number ENDS: the model has to emit a terminator (',', '}'),
    which you then strip.
    """

    def allowed_mask(self) -> BoolMask:
        """TODO: start from vocab.number_chars_mask, then keep only
        tokens whose text keeps a valid partial number."""
        raise NotImplementedError

    def is_complete(self) -> bool:
        """TODO: a terminator was emitted after a complete number."""
        raise NotImplementedError

    def value(self) -> float:
        """TODO: convert to float (the subject expects 2.0, not 2)."""
        raise NotImplementedError
