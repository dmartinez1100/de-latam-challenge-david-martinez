# pylint: disable=W1514,R0801
"""Module providing a function for challenge Q1 focused on memory."""
from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Function with code of Q1 focused on memory."""

    # Se inicializa un defaultdict con valor por defecto en 0 (int)
    count_dates_users = defaultdict(Counter)

    # Se abre el archivo, será de solo lectura "r"
    with open(file_path, "r") as tweets_file:

        # Para cada linea del archivo, se parsea a JSON y
        # se extrae unicamente lo necesario
        # - fecha unicamente hasta el día (facilita agrupamientos)
        # - usuario que se encuentra anidado dentro de lainformacion de usuario
        for tweet in tweets_file:
            tweet = json.loads(tweet)
            _date = tweet["date"].split("T")[0]
            _user = tweet["user"]["username"]

            # se actualiza el contador cada vez que un usuario tweeteó en x día
            count_dates_users[_date].update([_user])

        # Cerramos el archivo ya que se procesó todo
        tweets_file.close()

        # Sumando el contador de cada fecha, obtenemos
        # el total de tweets en el día especifico
        # tomamos este valor como llave para ordenar las fechas
        # y sacamos las 10 fechas más grandes
        top_dates = sorted(count_dates_users.items(),
                           key=lambda date_count: sum(date_count[1].values())
                           )[-10:]

        # usamos map() con el top de fechas para tomar el usuario
        # más comun de cada contador, además de transformar a
        # datetime la fecha ya que asi lo pide el ejercicio.
        top_dates_user = map(
            lambda dt: (datetime.fromisoformat(dt[0]),
                        dt[1].most_common(1)[0][0]
                        ),
            top_dates)

        # finalmente ordenamos el top 10
        # note que seordenna una lista de 10 elementos,
        # complejidad casi constate O(1), pero nos facilita
        # la lectura
        return sorted(top_dates_user)
