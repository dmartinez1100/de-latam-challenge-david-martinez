# pylint: disable=W1514
"""Module providing a function for challenge Q3 focused on time."""
from typing import List, Tuple
from collections import Counter
import re
import json
from concurrent.futures import ThreadPoolExecutor


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q3 focused on time."""
    def count_users(tws):
        n_users = Counter()
        for tweet in tws:
            tw_content = json.loads(tweet)["content"]
            n_users.update(
                user.replace("@", "").upper()
                for user
                in re.findall(r'@\w{4,15}\b', tw_content)
                )

        return n_users

    n_users = Counter()
    n_threads = 3
    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()
        ln_count = len(tweets)
        chunk_sz = ln_count // n_threads
        chunks = [
            tweets[(i * chunk_sz): ((i + 1) * chunk_sz if i < 4 else ln_count)]
            for i
            in range(5)
            ]

        # Procesar las partes en paralelo
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(
                count_users,
                chunks
                ))

        for resultado in resultados:
            n_users.update(resultado)

        return n_users.most_common(10)
