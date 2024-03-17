# pylint: disable=W1514,R0801
"""Module providing a function for challenge Q2 focused on memory."""
from typing import List, Tuple
from collections import Counter
import json
import emoji


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q2 focused on memory."""

    # se inicializa un contador para juntar todos los resultados
    n_emojis = Counter()

    # Se abre el archivo, será de solo lectura "r"
    with open(file_path, "r") as tweets_file:

        # Se itera sobre cada linea del archivo para convertir a
        # json y contar los emojis del contenido de cada tweet
        for tweet in tweets_file:

            # Noté tweets anidados en el archivo (quoted_tweet), sin embargo
            # no los tendré en cuenta, será una mejora que deberá hacerse.
            tweet_content = json.loads(tweet)["content"]

            # actualizo mi conntador de emojis con los resultados de cada tweet
            n_emojis.update(
                emo["emoji"]
                for emo
                in emoji.emoji_list(tweet_content)
                )

        # finalmete nos aprovechamos del Counter como estructura de datos
        # para obtener los 10 más comunes
        return n_emojis.most_common(10)
