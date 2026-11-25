"""High level: one natural-language prompt -> one FunctionCall."""
# from src.constraints import NumberConstraint
from llm_sdk import Small_LLM_Model

from src.constraints import Constraint
from src.decoder import ConstrainedDecoder
from src.models import FunctionCall, FunctionDefinition, ParameterSpec
from src.vocabulary import Vocabulary


class FunctionCaller:
    """Chooses the function and its arguments with the LLM."""

    def __init__(
        self,
        model: Small_LLM_Model,
        vocab: Vocabulary,
        functions: list[FunctionDefinition],
    ) -> None:
        """Store dependencies and index functions by name."""
        self.model = model
        self.vocab = vocab
        self.functions = {f.name: f for f in functions}
        self.decoder = ConstrainedDecoder(model)

    def _encode(self, text: str) -> list[int]:
        """Text -> token ids (wraps model.encode, returns a plain list)."""
        tensor = self.model.encode(text)
        ids: list[int] = tensor[0].tolist()
        return ids

    def _constraint_for(self, spec: ParameterSpec) -> Constraint:
        """Return a fresh constraint matching a parameter type.

        TODO: one branch per supported type. This is THE place to
        touch when the evaluator asks you to support a new type.
        """

        raise NotImplementedError

    def call(self, user_prompt: str) -> FunctionCall:
        """Translate one prompt into a function call.

        TODO:
        Phase 1 - build context, ChoiceConstraint over function names.
        Phase 2 - for each parameter of the chosen function:
            append forced text ('", "parameters": {"a": ' ...),
            generate the value with _constraint_for(spec).
        Return a validated FunctionCall.
        """
        raise NotImplementedError
