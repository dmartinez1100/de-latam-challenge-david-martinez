# pylint: disable=W1514
"""Module providing a function for challenge Q3 focused on memory."""
from typing import List, Tuple
from collections import Counter
import re
import json


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q3 focused on memory."""

    n_users = Counter()
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            tw_content = json.loads(tweet)["content"]
            n_users.update(
                user.replace("@", "").upper()
                for user
                in re.findall(r'@\w{4,15}\b', tw_content)
                )

        return n_users.most_common(10)
