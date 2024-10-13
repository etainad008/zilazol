import re
import os

IMPORT_LINE = "from constants import"
FILE_PATH = "api\\constants.py"
CONSTANT_ASSIGNMENT_PATTERN = r"\b[A-Z_]+\b(?=\s*=[^=]*)"
SCREAMING_SNAKE_CASE_PATTERN = r"\b[A-Z_]+\b"


constants_re = None


def main():
    # get constants
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        constants = set(re.findall(CONSTANT_ASSIGNMENT_PATTERN, content))

    files = get_python_files("api")
    for file_path in files:
        if file_path == FILE_PATH:
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            file_constants = set(constants_re.findall(content))
            consts_constants = file_constants.intersection(constants)

            f.seek(0)
            lines = f.readlines()
            with open(file_path, "w", encoding="utf-8") as fw:
                for line in lines:
                    if line.startswith(IMPORT_LINE) and line.strip().endswith("*"):
                        fw.write(
                            f"{IMPORT_LINE} {", ".join(sorted(consts_constants))}\n"
                        )
                    else:
                        fw.write(line)


def get_python_files(dir_path: str):
    for root, _, files in os.walk(dir_path):
        return [os.path.join(root, file) for file in files if file.endswith(".py")]


if __name__ == "__main__":
    constants_re = re.compile(SCREAMING_SNAKE_CASE_PATTERN)
    main()
