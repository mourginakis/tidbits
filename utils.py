def slurp(path: str) -> str:
    """Read file into memory."""
    with open(path, 'r') as file:
        return file.read()


def spit(path: str, content: str) -> None:
    """Write content to file, creating file if it doesn't exist."""
    with open(path, 'a') as file:
        file.write(content)
