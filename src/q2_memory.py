# pylint: disable=W1514
"""Module providing a function for challenge Q2 focused on memory."""
from typing import List, Tuple
from collections import Counter
import json
import emoji


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q2 focused on memory."""
    n_emos = Counter()
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            tweet_content = json.loads(tweet)["content"]
            n_emos.update(
                emo["emoji"]
                for emo
                in emoji.emoji_list(tweet_content)
                )

        return n_emos.most_common(10)
