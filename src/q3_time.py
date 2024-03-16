from typing import List, Tuple
from collections import Counter
import re
import json
from concurrent.futures import ThreadPoolExecutor

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    
    def countemojis(tws):
        n_users = Counter()
        for tweet in tws:
            tw_content =  json.loads(tweet)["content"]
            n_users.update(user.replace("@", "").upper() for user in re.findall(r'@\w{4,15}\b', tw_content))

        return n_users

    n_users = Counter()
    n_threads = 3
    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()
        total_lines = len(tweets)
        lines_per_part = total_lines // n_threads

        # Procesar las partes en paralelo
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(countemojis, [
                tweets[(i * lines_per_part): ((i + 1) * lines_per_part if i < n_threads-1 else total_lines)] for i in range(n_threads)
            ]))
        
        for resultado in resultados:
            n_users.update(resultado)

        return n_users.most_common(10)