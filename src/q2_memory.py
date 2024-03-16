from typing import List, Tuple
from collections import Counter
import json
import emoji

def q2_memory(file_path: str) -> List[Tuple[str, int]]:

    n_emos = Counter()
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            a =  json.loads(tweet)
            n_emos.update(emo["emoji"] for emo in emoji.emoji_list(a["content"]))

        return n_emos.most_common(20)