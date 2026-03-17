import json


def read_json(filename: str) -> list[dict]:
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("JSON invalide", e.doc, e.pos)

    except FileNotFoundError:
        raise FileNotFoundError("File Not Found")

    except PermissionError:
        raise PermissionError("File can't be open")
