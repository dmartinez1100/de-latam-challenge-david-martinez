from typing import List, Tuple
from datetime import datetime
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def q1_time3(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Lee el archivo JSON en bloques de tamaño 'num_rows'
    df = pd.read_json(file_path, lines=True, convert_dates=False)
    #df_selected = df[['date', 'user']].copy()
    df['user'] = df['user'].apply(lambda x: x['username'])
    df['date'] = df['date'].apply(lambda x: x[:10])