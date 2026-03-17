def build_prompt(call: str, functions: dict[str]) -> str:
    p = "You have access to the following functions:\n"
    for func in functions:
        line = f"- {func['name']}: {func['description']}\n"
        p += line
    p += ("\nWhich function should be called for:"
               f" \"{call['prompt']}\" ?\n")
    return p
