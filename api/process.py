import re
from collections import defaultdict
import sys, io
from constants import *
from Levenshtein import jaro_winkler


# tokens which number of names divided by their number of occurrences above this threshold are taken into the final name.
TOKEN_RATIO_THRESHOLD = 0.33

# tokens which their Levenshtein ratio is above this are merged into a single token.
# we will take the longest among them.
TOKEN_SIMILARITY_THRESHOLD = 0.8


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

whitespace_pattern = re.compile(r"\s+|-")

blacklist = UNIT_HEBREW
blacklist_pattern = "|".join(map(re.escape, blacklist))

# dont ask, it works
pattern = rf"(\d+\.?\d*) ?({blacklist_pattern})\b(?!%)|\b({blacklist_pattern}) ?(\d+\.?\d*)\b(?!%)"
units_pattern = re.compile(pattern)


def derive_name(name_list: list[str]) -> str:
    """Gets the most "common" or logical name derived from the given name list.
    It is assumed that the names are whitespace-normalized (stripped with only single spaces).
    """
    name_count = len(name_list)
    derived_tokens = defaultdict(float)
    token_instances = defaultdict(list)  # list of indexes in tokens in each name
    merged_tokens = set()
    merging_tokens = set()

    # count all instances of each token
    for name in name_list:
        tokens = normalize_whitespace(units_pattern.sub("", name)).split(" ")
        for i in range(len(tokens)):
            token_instances[tokens[i]].append(i)

    token_list = list(token_instances.keys())
    for token in token_list:
        if token in merged_tokens:
            continue

        unmerged_tokens = [
            j for j in token_list if not j in merged_tokens and j != token
        ]

        similar_tokens = [
            other
            for other in unmerged_tokens
            if jaro_winkler(token, other, score_cutoff=TOKEN_SIMILARITY_THRESHOLD)
        ]

        if len(similar_tokens) != 0:
            # get the longest token
            merging_token = token
            longest_similar_token = max(similar_tokens, key=len)
            if len(longest_similar_token) > len(token):
                merging_token = longest_similar_token
                similar_tokens.remove(merging_token)
                similar_tokens.append(token)

            merging_tokens.add(merging_token)
            merged_tokens.add(merging_token)
            for similar_token in similar_tokens:
                merged_tokens.add(similar_token)

                # add instances of merged tokens
                token_instances[merging_token].extend(token_instances[similar_token])

    for token, indexes in token_instances.items():
        if token in merged_tokens and not token in merging_tokens:
            continue

        number_of_occurrences = len(indexes)
        if number_of_occurrences / name_count < TOKEN_RATIO_THRESHOLD:
            continue

        # average index - maybe give indexes which are abnormal less weight
        derived_tokens[token] = sum(indexes) / number_of_occurrences

        index_count = {i: indexes.count(i) for i in indexes}
        index_weights = {i: index_count[i] / number_of_occurrences for i in index_count}
        weighted_mean_sum = sum(
            key * index_count[key] * index_weights[key] for key in index_count
        )

        derived_tokens[token] = weighted_mean_sum / number_of_occurrences

    return " ".join(
        sorted(derived_tokens.keys(), key=lambda token: derived_tokens[token])
    )


def normalize_whitespace(text: str) -> str | None:
    if text:
        return whitespace_pattern.sub(
            " ", text.replace("-", " ").replace("&", " אנד ").strip()
        )
    return None
