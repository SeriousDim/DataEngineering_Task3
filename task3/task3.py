from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

from functions import dicts_to_json, sort_df, filter_df, get_statistics, get_frequencies


def parse_to_dict(text) -> dict:
    result = {}

    bs = BeautifulSoup(text, 'xml')
    star = bs.find('star')
    result['name'] = star.find('name').text.strip()
    result['constellation'] = star.find('constellation').text.strip()
    result['spectral'] = star.find('spectral-class').text.strip()
    result['radius'] = float(star.find('radius').text.strip())
    result['rotation'] = float(star.find('rotation').text.strip().split(' ')[0])
    result['age'] = float(star.find('age').text.strip().split(' ')[0])
    result['distance'] = float(star.find('distance').text.strip().split(' ')[0])
    result['magnitude'] = float(star.find('absolute-magnitude').text.strip().split(' ')[0])

    return result


path = Path("./3")
files = list(path.iterdir())

dicts = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    dicts.append(parse_to_dict(text))

output_path = '../outputs/task3'
dicts_to_json(dicts, f'{output_path}/task3.json')

df = pd.DataFrame(dicts)
sort_df(df, 'radius', f'{output_path}/sorted.csv')

filtered_df = df[df['age'] > 4]
filtered_df.to_csv(f'{output_path}/filtered.csv')

get_statistics(df, 'distance', f'{output_path}/distance_stats.json')
get_frequencies(df, 'spectral', f'{output_path}/spectral_freqs.json')
