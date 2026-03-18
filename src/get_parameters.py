import numpy as np
from typing import Any, Union
from llm_sdk.llm_sdk import Small_LLM_Model


def is_number_token(s: str) -> bool:
    """Check if a string represents a valid number token.

    Args:
        s: The string to check.

    Returns:
        True if the string is a valid number token, False otherwise.
    """
    if len(s) == 0:
        return False
    for c in s:
        if not (c.isdigit() or c == '.' or c == '-'):
            return False
    return True


def get_parameters(functions: list[dict[str, Any]], func_name: str,
                   model: Small_LLM_Model, vocs: dict[int, str],
                   token_ids: list[int]) -> dict[str, Union[str, float]]:
    """Extract parameters for a given function using the language model.

    Args:
        functions: A list of dictionaries describing available functions.
        func_name: The name of the function to extract parameters for.
        model: The language model used for generation.
        vocs: A dictionary mapping token IDs to strings.
        token_ids: The current list of token IDs.

    Returns:
        A dictionary of parameter names to their values (str or float).
    """
    for func in functions:
        if func['name'] == func_name:
            parameters: dict[str, Union[str, float]] = {}
            for param_name, param_info in func['parameters'].items():
                param_type = param_info['type']
                token = 0
                count = 0

                if param_type == "string":
                    context = f"\nArgument '{param_name}' = \""
                elif param_type == "number":
                    context = f"\nArgument '{param_name}' = "
                encoded = model.encode(context)[0].tolist()
                token_ids += encoded
                if param_type == "string":
                    if count > 100:
                        break
                    param = ""
                    while True:
                        logits = model.get_logits_from_input_ids(token_ids)
                        token = logits.index(max(logits))
                        # print(f"token: {repr(vocs[token])}")
                        if ('"' in vocs[token] or 'Ċ' in vocs[token] or
                                len(param) > 50):
                            break
                        token_ids.append(token)
                        param += vocs[token]
                        param = param.replace("Ġ", " ")
                        count += 1
                    parameters[param_name] = param

                elif param_type == "number":
                    param = ""
                    stop_tokens = [",", "}", "?", " "]
                    while vocs[token] not in stop_tokens:
                        if count > 20:
                            break
                        logits = model.get_logits_from_input_ids(token_ids)
                        for i in range(0, len(logits)):
                            if i not in vocs:
                                logits[i] = -np.inf
                                continue
                            allowed = (is_number_token(vocs[i]) or
                                       vocs[i] in stop_tokens)
                            if not allowed:
                                logits[i] = -np.inf
                        token = logits.index(max(logits))
                        if vocs[token] in stop_tokens:
                            break
                        token_ids.append(token)
                        param += vocs[token]
                        count += 1
                    parameters[param_name] = float(param)
    return parameters
