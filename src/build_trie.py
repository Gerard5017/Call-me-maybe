from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model


def build_trie(
    functions: list[dict[str, Any]],
    model: Small_LLM_Model
) -> dict[int, Any]:
    """Build a trie structure from function names using the model's tokenizer.

    Args:
        functions: A list of dictionaries describing available functions.
        model: The language model used for tokenization.

    Returns:
        A nested dictionary representing the trie of function name tokens.
    """
    trie: dict[int, Any] = {}
    for func in functions:
        tokens = model.encode(func['name'])[0].tolist()
        node = trie
        for token in tokens:
            if token not in node:
                node[token] = {}
            node = node[token]
    return (trie)
