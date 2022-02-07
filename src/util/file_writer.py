import os


def write_to_file(content: str, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(content)
