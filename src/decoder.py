"""Generic constrained generation loop (type-agnostic)."""

from typing import Any

import numpy as np

from llm_sdk import Small_LLM_Model

from src.constraints import Constraint
from src.errors import GenerationError


class ConstrainedDecoder:
    """Runs the model token by token under a constraint."""

    def __init__(self, model: Small_LLM_Model, max_tokens: int = 64) -> None:
        """Store the model and the safety limit per value."""
        self.model = model
        self.max_tokens = max_tokens

    def generate(
        self,
        input_ids: list[int],
        constraint: Constraint,
    ) -> tuple[Any, list[int]]:
        """Generate one value.

        Args:
            input_ids: Context so far (prompt + forced JSON).
            constraint: Decides which tokens are allowed.

        Returns:
            The Python value, and the context extended with the
            generated tokens (needed to generate the next value).

        Raises:
            GenerationError: max_tokens reached, or no token allowed.
        """
        ids = list(input_ids)
        for _ in range(self.max_tokens):
            if constraint.is_complete():
                return constraint.value(), ids
            logits = np.asarray(
                self.model.get_logits_from_input_ids(ids), dtype=np.float32)
            mask = constraint.allowed_mask()
            if not mask.any():
                raise GenerationError(
                    f"no token allowed after {constraint.generated!r}")
            logits[~mask] = -np.inf
            token = int(np.argmax(logits))
            ids.append(token)
            constraint.advance(token)
        if constraint.is_complete():
            return constraint.value(), ids
        raise GenerationError(
            f"value not finished after {self.max_tokens} tokens: "
            f"{constraint.generated!r}")
