"""Builds the text context given to the LLM.

The prompt helps the model make GOOD choices; the constraints guarantee
VALID output. Never rely on the prompt for structure.
"""

from src.models import FunctionDefinition


def build_context(
    user_prompt: str,
    functions: list[FunctionDefinition],
) -> str:
    """Return the text the model continues from.

    TODO: describe the available functions (name, description,
    parameter names/types), then the user request, then the beginning
    of the JSON answer (e.g. '{"name": "'). Experiment: the exact
    wording changes accuracy a lot with a 0.6B model.
    Look up Qwen3's chat template if you want to use it.
    """
    raise NotImplementedError
