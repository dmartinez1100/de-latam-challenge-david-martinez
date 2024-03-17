# pylint: disable=W1514
"""Module providing a function for challenge Q1 focused on time."""
from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Function with code of Q1 focused on time."""
    counter_dates = Counter()
    counter_dates_user = defaultdict(Counter)
    with open(file_path, "r") as tweets_file:
        for tweet in tweets_file:
            tweet = json.loads(tweet)
            _date = tweet["date"].split("T")[0]
            _user = tweet["user"]["username"]
            counter_dates.update(_date)
            counter_dates_user[_date].update([_user])
        tweets_file.close()
        return sorted([
            (datetime.fromisoformat(f[0]),
             counter_dates_user[f[0]].most_common(1)[0][0]
             )
            for f in counter_dates.most_common(10)
            ])
