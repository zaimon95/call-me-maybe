"""Pick exactly one string among a fixed set (e.g. function names)."""

from src.constraints.base import Constraint
from src.vocabulary import BoolMask, Vocabulary


class ChoiceConstraint(Constraint):
    """Allows only tokens keeping the text a prefix of some option."""

    def __init__(self, vocab: Vocabulary, options: list[str]) -> None:
        """Store the options.

        TODO: think about options that are prefixes of each other
        (fn_add / fn_add_numbers): how do you know you're complete?
        """
        super().__init__(vocab)
        self.options = options

    def allowed_mask(self) -> BoolMask:
        """TODO: token allowed if generated + token_text is a prefix
        of at least one option. Avoid testing 150k tokens in pure
        Python at each step: which tokens can possibly match?"""
        raise NotImplementedError

    def is_complete(self) -> bool:
        """TODO: generated equals one option exactly (and no ambiguity)."""
        raise NotImplementedError

    def value(self) -> str:
        """Return the chosen option."""
        raise NotImplementedError
