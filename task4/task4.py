from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

from functions import dicts_to_json, sort_df, filter_df, get_statistics, get_frequencies


def parse_to_dict(text):
    result = []

    bs = BeautifulSoup(text, 'xml')
    cloths = bs.find_all('clothing')
    for c in cloths:
        parsed = {}
        tags = c.find_all()
        for t in tags:
            parsed[t.name] = t.text.strip()
        result.append(parsed)

    return result


path = Path("./4")
files = list(path.iterdir())

dicts = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    dicts += parse_to_dict(text)

df = pd.DataFrame(dicts)
df[['price', 'rating', 'reviews']] = df[['price', 'rating', 'reviews']].astype(float)
print(df.info())

output_path = '../outputs/task4'
dicts_to_json(dicts, f'{output_path}/task4.json')

sort_df(df, 'name', f'{output_path}/sorted.csv')

filtered_df = df[df['new'] == '+']
filtered_df.to_csv(f'{output_path}/filtered.csv')

get_statistics(df, 'reviews', f'{output_path}/reviews_stats.json')
get_frequencies(df, 'color', f'{output_path}/color_freqs.json')


