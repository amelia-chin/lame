def a_clean(string: str) -> str:
    output = ""
    for char in string:
        if char == "'":
            output += "'"
        output += char
    return output