"""Common interface of every constraint."""

from abc import ABC, abstractmethod
from typing import Any

from src.vocabulary import BoolMask, Vocabulary


class Constraint(ABC):
    """A state machine over generated text.

    The decoder does not know which type it generates: it only asks
    the constraint which tokens are allowed, feeds it the chosen one,
    and stops when the constraint is complete.
    """

    def __init__(self, vocab: Vocabulary) -> None:
        """Store the vocabulary and reset the generated text."""
        self.vocab = vocab
        self.generated: str = ""

    @abstractmethod
    def allowed_mask(self) -> BoolMask:
        """Return True for every token id allowed at this step."""

    def advance(self, token_id: int) -> None:
        """Update the state after a token has been accepted.

        TODO: default behaviour = append the token text to
        self.generated; override if a constraint needs more state.
        """
        raise NotImplementedError

    @abstractmethod
    def is_complete(self) -> bool:
        """Return True when the value is finished."""

    @abstractmethod
    def value(self) -> Any:
        """Convert the generated text into the final Python value.

        Example: "2" -> 2.0 for a number, "true" -> True for a boolean.
        """
