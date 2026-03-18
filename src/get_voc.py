from llm_sdk.llm_sdk import Small_LLM_Model
from .read_json import read_json


def get_voc(model: Small_LLM_Model) -> dict[int, str]:
    """Load the vocabulary from the model's tokenizer file.

    Args:
        model: The language model instance.

    Returns:
        A dictionary mapping token IDs to token strings.
    """
    voc_file = model.get_path_to_tokenizer_file()
    vocs_content = read_json(voc_file)
    vocs_dict = vocs_content["model"]["vocab"]
    id_to_token = {v: k for k, v in vocs_dict.items()}
    max_id = max(id_to_token.keys()) + 1
    for i in range(max_id):
        if i not in id_to_token:
            id_to_token[i] = ""
    return id_to_token
