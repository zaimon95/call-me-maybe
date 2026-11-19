"""Generate a JSON boolean."""

from src.constraints.base import Constraint
from src.vocabulary import BoolMask


class BooleanConstraint(Constraint):
    """Allows only prefixes of "true" / "false".

    TODO: this is a ChoiceConstraint in disguise - can you reuse it?
    """

    def allowed_mask(self) -> BoolMask:
        """TODO"""
        raise NotImplementedError

    def is_complete(self) -> bool:
        """TODO"""
        raise NotImplementedError

    def value(self) -> bool:
        """TODO"""
        raise NotImplementedError
