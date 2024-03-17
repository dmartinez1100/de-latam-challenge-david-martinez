# pylint: disable=W1514,R0801
"""Module providing a function for challenge Q2 focused on time."""
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from collections import Counter
import json
import emoji


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """Function with code of Q2 focused on time."""

    # funcion que recibe una lista de tweets y retorna el conteo de cada emoji
    # a lo largo de toda la lista
    def count_emojis(tws):

        # se inicializa un counter para los emojis, y se itera sobre el
        # contenido de cada tweet.
        # Noté tweets anidados en el archivo (quoted_tweet), sin embargo
        # no los tendré en cuenta, será una mejora que deberá hacerse.
        n_emojis = Counter()
        for tweet in tws:
            tw_content = json.loads(tweet)["content"]

            # Actualizo el contador con todos los emojis encontrados, para esto
            # uso lafunción emoji_list de la libreria "emoji".
            n_emojis.update(
                _emoji["emoji"]
                for _emoji
                in emoji.emoji_list(tw_content)
                )

        # Se retorna el contador de los emojis
        return n_emojis

    # variable para el número de hilos que se ejecutaran en paralelo
    # Deberia ser una constante global para que sea reutilizada
    n_threads = 3

    # se inicializa un contador para juntar todos los resultados
    n_emojis = Counter()

    # Se abre el archivo, será de solo lectura "r"
    # en este caso vamos a leer todo el archivo de inmediato
    # esto subirá enormemente el consumo de memoria, pero será util
    # para partir los datos en N partes y ponerlos a procesar de forma
    # paralela
    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()

        # Cerramos el archivo porque ya fue procesado y  cargado en
        # memoria
        tweets_file.close()

        ln_count = len(tweets)

        # Dado el número de hilos  que se requiere, se obtiene tamaño
        # de cada chunk y se hace slicing sobre la lista de tweets
        chunk_sz = ln_count // n_threads
        chunks = [
            tweets[(i * chunk_sz): ((i + 1) * chunk_sz
                                    if i < n_threads - 1
                                    else ln_count)]
            for i
            in range(n_threads)
            ]

        # Como ya tenemos la data dividida en chunks, eliminamos la
        # lista de tweets original, esto libera memoria
        del tweets

        # Se procesa en paralelo cada chunk, es decir, cada chunk
        # será mapeado con la funciñon count_emojis()
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(
                count_emojis,
                chunks
                ))

        # Note que cada resultado del mapper nos retornna un contador,
        # por lo que los juntamos todos.
        for resultado in resultados:
            n_emojis.update(resultado)

        # finalmete nos aprovechamos del Counter como estructura de datos
        # para obtener los 10 emmojis más comunes
        return n_emojis.most_common(10)
