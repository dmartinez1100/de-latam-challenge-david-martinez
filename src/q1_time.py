# pylint: disable=W1514,R0801
"""Module providing a function for challenge Q1 focused on time."""
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json
from functools import reduce


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Function with code of Q1 focused on time."""

    # función que toma un chunk (lista de tweets) y los transforma
    # retorna un top 10 local para el chunk, junto con los usuarios
    # que escribieron tweets en esos días
    def get_top_10(tws):

        # Se inicializa un defaultdict con valor por defecto un objeto contador
        # las llaves serán fechas (AAAA-MM-DD) en las que se han escrito tweets
        # y en cada valor se irán contado los usuarios que escriben cada día
        count_dates_users = defaultdict(Counter)

        # Para cada tweet, se parsea a JSON y
        # se extrae unicamente lo necesario
        # - fecha unicamente hasta el día (facilita agrupamientos)
        # - usuario que se encuentra anidado dentro de lainformacion de usuario
        for tweet in tws:
            tweet = json.loads(tweet)
            _date = tweet["date"].split("T")[0]
            _user = tweet["user"]["username"]
            count_dates_users[_date].update([_user])

        # Sumando el contador de cada fecha, obtenemos
        # el total de tweets en el día especifico,
        # tomamos este valor como llave para ordenar las fechas
        # y sacamos las 10 más grandes según el total
        top_dates = sorted(count_dates_users.items(),
                           key=lambda date_count: sum(date_count[1].values())
                           )[-10:]

        # retornamos el top_10 local
        # note que no se ordena por fecha, porque pasará por un reducer y puede
        # que se siga iterando y pierda el orden dado.
        return top_dates

    # función usada para reducir el resultado posterior a mapear cada chunk
    # recibe 2 listas de top_10 y retorna una lista top_10 resultante de
    # haber combinado las dos enntradas de la función.

    # -- Note que esta función es análoga a get_top_10(), una mejora posterior
    # es juntarlas en una sola función, ya que solo cambia el tipo de
    # dato etrante y la forma en como se itera para rellenar count_dates_users,
    # puede haacerce un tratamiento condicional dependiento de la entrada. ---
    def reduce_top_10(top10_1, top10_2):

        # Se inicializa un defaultdict con valor por defecto un objeto contador
        # las llaves serán fechas (AAAA-MM-DD) en las que se han escrito tweets
        # y en cada valor se irán contado los usuarios que escriben cada día
        count_dates_users = defaultdict(Counter)

        # Se rellena count_dates_users con la información de ambos top_10
        for _date, _user_counter in (top10_1 + top10_2):
            count_dates_users[_date].update(_user_counter)

        # Sumando el contador de cada fecha, obtenemos
        # el total de tweets en el día especifico,
        # tomamos este valor como llave para ordenar las fechas
        # y sacamos las 10 más grandes según el total.
        top_dates = sorted(count_dates_users.items(),
                           key=lambda date_count: sum(date_count[1].values()),
                           reverse=True
                           )[:10]

        # retornamos el top_10 local
        # note que no se ordena por fecha, porque puede que se siga
        # iterando y reduciendo.
        return top_dates

    # variable para el número de hilo que se ejecutaran en paralelo
    # Deberia ser una constante global para que sea reutilizada
    n_threads = 3

    # Se abre el archivo, será de solo lectura "r"
    # en este caso vamos a leer todo el archivo de inmediato
    # esto subirá enormemente el consumo de memoria, pero será util
    # para partir los datos en N partes y ponerlas a procesar de forma
    # paralela
    with open(file_path, "r") as tws_file:
        tws = tws_file.readlines()
        ln_count = len(tws)

        # Dado el número de hilos  que se requiere, se obtiene tamaño
        # de cada chunk y se hace slicing sobre la lista de tweets
        chunk_sz = ln_count // n_threads
        chunks = [
            tws[(i * chunk_sz): ((i + 1) * chunk_sz
                                 if i < n_threads - 1
                                 else ln_count)]
            for i
            in range(n_threads)
            ]

        # Se procesa en paralelo cada chunk, es decir, cada chunk
        # será mapeado con la funciñon get_top_10()
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada chunk
            resultados = list(executor.map(
                get_top_10,
                chunks
                ))

        # una vez obtenemos todos los N top_10 locales, los pasamos
        # por reduce_top_10(), que está hecha para integrarse con
        # reduce(), dados los N top_10 locales, reduce retornará un
        # solo top_10
        resultados = reduce(reduce_top_10, resultados)

        # finalmente, usamos map() con el top de fechas para tomar
        # el usuario más comun de cada contador, además se transforma
        # a datetime la fecha ya que asi lo pide el ejercicio.
        top_dates_user = list(map(
            lambda dt: (datetime.fromisoformat(dt[0]),
                        dt[1].most_common(1)[0][0],
                        ),
            resultados))

        # finalmente ordenamos el top 10, note que se ordena una lista
        # de 10 elementos ... complejidad casi constate O(1), pero nos
        # facilita la lectura para el usuario.
        return sorted(top_dates_user)
