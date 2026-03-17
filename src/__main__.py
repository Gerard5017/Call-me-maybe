from .read_json import read_json
from .build_prompt import build_prompt
from llm_sdk.llm_sdk import Small_LLM_Model


def main():
    try:
        model = Small_LLM_Model()
        calling = read_json("data/input/function_calling_tests.json")
        functions = read_json("data/input/functions_definition.json")
        prompts = []
        for call in calling:
            prompts.append(build_prompt(call, functions))
        for c in prompts:
            model.encode(c)
    except BaseException as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
