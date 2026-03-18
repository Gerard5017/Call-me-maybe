import os
import json
import numpy as np
from .get_voc import get_voc
from .read_json import read_json
from .parse_args import parse_args
from .build_trie import build_trie
from .build_prompt import build_prompt
from .get_parameters import get_parameters
from llm_sdk.llm_sdk import Small_LLM_Model


def main() -> None:
    """Main entry point for the function calling application.

    Parses arguments, loads data, builds the trie, processes prompts,
    extracts function calls and parameters, and saves results to a file.
    """
    try:
        args = parse_args()
        model = Small_LLM_Model()
        vocs = get_voc(model)
        calling = read_json(args.input)
        functions = read_json(args.functions_definition)
        trie = build_trie(functions, model)
        prompts = []
        calls = []
        for call in calling:
            calls.append(call["prompt"])
            prompts.append(build_prompt(call, functions))
        results = []
        for c in prompts:
            tokens = []
            encoded = model.encode(c)
            token_ids = encoded[0].tolist()
            node = trie
            max_tokens = 50
            token_count = 0
            last_valid_func = None
            while node:
                if token_count > max_tokens:
                    func_name = functions[0]['name']
                    break
                logits = model.get_logits_from_input_ids(token_ids)
                for i in range(0, len(logits)):
                    if i not in node.keys():
                        logits[i] = -np.inf
                token = logits.index(max(logits))
                tokens.append(token)
                token_ids.append(token)
                node = node[token]
                token_count += 1
                if not node:
                    last_valid_func = model.decode(tokens)
            func_name = model.decode(tokens)
            func_name = last_valid_func or func_name
            parameters = get_parameters(functions, func_name, model,
                                        vocs, token_ids)
            call_result = {
                "prompt": calls.pop(0),
                "name": func_name,
                "parameters": parameters
            }
            results.append(call_result)
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as file:
            json.dump(results, file, indent=2)

    except Exception as e:
        print(f"ERROR: {e}")

    except KeyboardInterrupt:
        print("\nProgram was killed")


if __name__ == "__main__":
    main()
