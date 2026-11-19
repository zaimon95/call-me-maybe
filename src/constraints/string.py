"""Generate the content of a JSON string (opening quote already forced)."""

from src.constraints.base import Constraint
from src.vocabulary import BoolMask


class StringConstraint(Constraint):
    """Allows string-safe tokens until the closing quote.

    TODO: handle escapes (\\" and \\\\), forbid raw control
    characters, and decide what to do with tokens containing
    the closing quote plus other characters ('o",').
    """

    def allowed_mask(self) -> BoolMask:
        """TODO: string_safe_mask + tokens that close the string."""
        raise NotImplementedError

    def is_complete(self) -> bool:
        """TODO: the closing (unescaped) quote has been emitted."""
        raise NotImplementedError

    def value(self) -> str:
        """TODO: strip the closing quote and unescape (json.loads?)."""
        raise NotImplementedError
