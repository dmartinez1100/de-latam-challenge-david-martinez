from typing import List, Tuple
from datetime import datetime
import json
from collections import defaultdict, counter
from concurrent.futures import ThreadPoolExecutor

def q1_time2(file_path: str) -> List[Tuple[datetime.date, str]]:

    def maptws(tws):
        count_dates_users = defaultdict(lambda : defaultdict(int))
        for tweet in tws:
            a = json.loads(tweet) if type(tweet) == str else tweet
            count_dates_users[a["date"].split("T")[0]][a["user"]["username"]] += 1
        top_dates = sorted(count_dates_users.items(), key=lambda date_cout: sum(date_cout[1].values()))[:10]
        top_dates_user = list(map( lambda dt: (datetime.fromisoformat(dt[0]), max(count_dates_users[dt[0]].items(), key=lambda user: user[1])[0]), top_dates))
        return top_dates_user

    with open(file_path, "r") as tweets_file:
        tweets = tweets_file.readlines()
        total_lines = len(tweets)
        lines_per_part = total_lines // 5
        
        
        # Procesar las partes en paralelo
        with ThreadPoolExecutor() as executor:
            # Mapear la función de procesamiento a cada parte del archivo
            resultados = list(executor.map(maptws, [
                tweets[(i * lines_per_part): ((i + 1) * lines_per_part if i < 4 else total_lines)] for i in range(5)
            ]))
        
        resultado_final = []
        for resultado in resultados:
            resultado_final.extend([{"date":str(res[0]), "user":{"username":res[1]}} for res in resultado])
        #tweets_file.close()
    
        return maptws(resultado_final)