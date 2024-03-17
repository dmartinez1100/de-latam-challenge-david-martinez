# pylint: disable=W1514
"""Module providing a function for challenge Q2 focused on time."""
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from collections import Counter
import json
import emoji


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q2 focused on time."""
    def countemojis(tws):
        n_emos = Counter()
        for tweet in tws:
            tw_content = json.loads(tweet)["content"]
            n_emos.update(emo["emoji"] for emo in emoji.emoji_list(tw_content))
        return n_emos

    n_emos = Counter()
    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()
        ln_count = len(tweets)
        chunk_sz = ln_count // 5
        chunks = [
            tweets[(i * chunk_sz): ((i + 1) * chunk_sz if i < 4 else ln_count)]
            for i
            in range(5)
            ]

        # Procesar las partes en paralelo
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(
                countemojis,
                chunks
                ))

        for resultado in resultados:
            n_emos.update(resultado)

        return n_emos.most_common(10)
