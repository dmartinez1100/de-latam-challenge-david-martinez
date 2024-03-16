from typing import List, Tuple
from collections import Counter
import json
import emoji
from concurrent.futures import ThreadPoolExecutor

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    
    def countemojis(tws):
        n_emos = Counter()
        for tweet in tws:
            tw_content =  json.loads(tweet)["content"]
            n_emos.update(emo["emoji"] for emo in emoji.emoji_list(tw_content))
        return n_emos

    n_emos = Counter()
    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()
        total_lines = len(tweets)
        lines_per_part = total_lines // 5

        # Procesar las partes en paralelo
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(countemojis, [
                tweets[(i * lines_per_part): ((i + 1) * lines_per_part if i < 4 else total_lines)] for i in range(5)
            ]))
        
        for resultado in resultados:
            n_emos.update(resultado)

        return n_emos.most_common(20)