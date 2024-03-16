from typing import List, Tuple
from datetime import datetime
from collections import defaultdict
import json

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    count_dates_users = defaultdict(lambda : defaultdict(int))
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            a =  json.loads(tweet)
            count_dates_users[a["date"].split("T")[0]][a["user"]["username"]] += 1
        tweets_file.close()
        
        top_dates = sorted(count_dates_users.items(), key=lambda date_count: sum(date_count[1].values()))[-10:]
        top_dates_user = list(map( lambda dt: (datetime.fromisoformat(dt[0]), max(count_dates_users[dt[0]].items(), key=lambda user: user[1])[0]), top_dates))
        return sorted(top_dates_user)