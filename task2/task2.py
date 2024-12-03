from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

from functions import dicts_to_json, sort_df, filter_df, get_statistics, get_frequencies


def parse_to_dict(text) -> list[dict]:
    result = []

    bs = BeautifulSoup(text, 'html.parser')
    product_items = bs.find_all("div", {"class": "product-item"})
    for item in product_items:
        item_obj = {}
        item_obj['id'] = item.find('a')['data-id']
        item_obj['image'] = item.find('img')['src']
        item_obj['title'] = item.find('span').text.strip()
        item_obj['price'] = int(''.join(item.find('price').text.strip().split(' ')[:-1]))
        item_obj['bonuses'] = int(item.find('strong').text.strip().split(' ')[2])

        ul = item.find('ul')
        li_list = ul.find_all('li')
        for li in li_list:
            item_obj[li['type']] = li.text.strip().split(' ')[0]

        result.append(item_obj)

    return result


path = Path("./2")
files = list(path.iterdir())

dicts = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    dicts += parse_to_dict(text)

dicts_to_json(dicts, '../outputs/task2/task2.json')

df = pd.DataFrame(dicts)
sort_df(df, 'id', '../outputs/task2/sorted.csv')

filtered_df = df[df['processor'].notna()]
filtered_df.to_csv('../outputs/task2/filtered.csv')

get_statistics(df, 'price', '../outputs/task2/price_stats.json')
get_frequencies(df, 'resolution', '../outputs/task2/resolution_freqs.json')
