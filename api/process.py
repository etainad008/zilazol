import re
from collections import defaultdict
import sys, io
from constants import *


# tokens which number of names divided by their number of occurrences above this threshold are taken into the final name
TOKEN_RATIO_THRESHOLD = 0.5


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

whitespace_pattern = re.compile(r"\s+")

blacklist = UNIT_HEBREW
blacklist_pattern = "|".join(map(re.escape, blacklist))
pattern = (
    rf"(\d+\.?\d*) ?({blacklist_pattern})(?!%)|({blacklist_pattern}) ?(\d+\.?\d*)(?!%)"
)
units_pattern = re.compile(pattern)


def derive_name(name_list: list[str]) -> str:
    """Gets the most "common" or logical name derived from the given name list.
    It is assumed that the names are whitespace-normalized (stripped with only single spaces).
    """
    derived_tokens = defaultdict(float)
    name_count = len(name_list)
    token_instances = defaultdict(list)  # list of indexes in tokens in each name

    for name in name_list:
        tokens = normalize_whitespace(units_pattern.sub("", name)).split(" ")
        for i in range(len(tokens)):
            token_instances[tokens[i]].append(i)

    for token, indexes in token_instances.items():
        number_of_occurrences = len(indexes)
        if number_of_occurrences / name_count < TOKEN_RATIO_THRESHOLD:
            continue

        # average index
        derived_tokens[token] = sum(indexes) / number_of_occurrences

    return " ".join(
        sorted(derived_tokens.keys(), key=lambda token: derived_tokens[token])
    )


def normalize_whitespace(text: str) -> str | None:
    return whitespace_pattern.sub(" ", text.strip()) if text else None
