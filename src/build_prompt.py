from typing import Any


def build_prompt(call: dict[str, str], functions: list[dict[str, Any]]) -> str:
    """Build a prompt for function calling based on the call and available
    functions.

    Args:
        call: A dictionary containing the prompt to be processed.
        functions: A list of dictionaries describing available functions.

    Returns:
        The constructed prompt string.
    """
    p = "You have access to the following functions:\n"
    for func in functions:
        line = f"- {func['name']}: {func['description']}\n"
        p += line
    p += ("\nWhich function should be called for:"
          f" \"{call['prompt']}\" ?\n")
    return p
