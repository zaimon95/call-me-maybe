"""Mapping between token ids and the real text they represent.

Qwen uses byte-level BPE: the vocab file stores tokens with special
characters ("Ġ" for a space, "Ċ" for a newline...). Constraints must
compare against the REAL text, so this module decodes every token once
at startup and precomputes numpy masks used at each generation step.
"""

import numpy as np
import numpy.typing as npt


BoolMask = npt.NDArray[np.bool_]


class Vocabulary:
    """Decoded vocabulary plus precomputed token categories."""

    def __init__(self, vocab_path: str, vocab_size: int) -> None:
        """Load the vocab file and build all lookup structures.

        Args:
            vocab_path: Path returned by get_path_to_vocab_file().
            vocab_size: Number of logits returned by the model (can be
                larger than the vocab file: extra ids are never valid).

        TODO:
        1. Load the JSON (string -> id).
        2. Build the byte-level decoding table (search "GPT-2
           bytes_to_unicode") and convert each token to its real text.
        3. Store self.texts: list[str] indexed by id ("" if unknown).
        4. Call self._build_masks().
        """
        self.texts: list[str] = []
        self.size: int = vocab_size
        raise NotImplementedError

    def _build_masks(self) -> None:
        """Precompute boolean masks over the whole vocabulary.

        TODO: e.g. self.number_chars_mask (tokens made only of
        characters that can appear in a number), self.string_safe_mask
        (no unescaped quote, no control char)... One True/False per id.
        Ask yourself which masks the constraints really need.
        """
        raise NotImplementedError

    def text(self, token_id: int) -> str:
        """Return the real text of one token."""
        raise NotImplementedError
