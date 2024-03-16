from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json
    
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    n_dates = Counter()
    n_dates_2 = defaultdict(Counter)
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            a =  json.loads(tweet)
            n_dates.update([a["date"].split("T")[0]])
            n_dates_2[a["date"].split("T")[0]].update( [a["user"]["username"]] )
        tweets_file.close()
        return sorted([(datetime.fromisoformat(f[0]), n_dates_2[f[0]].most_common(1)[0][0]) for f in n_dates.most_common(10) ])