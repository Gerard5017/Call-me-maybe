import json
from typing import Any


def read_json(filename: str) -> Any:
    """Read and parse a JSON file.

    Args:
        filename: The path to the JSON file to read.

    Returns:
        The parsed JSON data.

    Raises:
        json.JSONDecodeError: If the file contains invalid JSON.
        FileNotFoundError: If the file does not exist.
        PermissionError: If there is a permission issue accessing the file.
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("JSON invalide", e.doc, e.pos)

    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

    except PermissionError:
        raise PermissionError("File can't be open")
