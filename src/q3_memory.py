# pylint: disable=W1514
"""Module providing a function for challenge Q3 focused on memory."""
from typing import List, Tuple
from collections import Counter
import re
import json


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q3 focused on memory."""

    # se inicializa un contador para juntar todos los resultados
    n_users = Counter()

    # Se abre el archivo, será de solo lectura "r"
    with open(file_path, "r") as tweets_file:

        # Se itera sobre cada linea del archivo para convertir a
        # json y contar los usuarios etiquetados en el contenido de cada tweet
        for tweet in tweets_file:

            # Noté tweets anidados en el archivo (quoted_tweet), sin embargo
            # no los tendré en cuenta, será una mejora que deberá hacerse.
            tw_content = json.loads(tweet)["content"]

            # dado el contenido de un tweet, por medio de regex se obtienen las
            # coincidencias de usuarios y se ingresan al contador.
            # Para la expresiñón regular usé 3 suposiciones obtenidas de la
            # documentación de X
            # --- la longitud de un usuario debe está 4 y 15 caracteres (regex)
            # --- Solo se permite caracteres alfanumericos y "_" (regex)
            # --- los usuarios son caseinsensitive (.upper() en el contador)
            n_users.update(
                user.replace("@", "").upper()
                for user
                in re.findall(r'@\w{4,15}\b', tw_content)
                )

        # finalmete nos aprovechamos del Counter como estructura de datos
        # para obtener los 10 usuarios más etiquetados
        return n_users.most_common(10)
