from pathlib import Path

from bs4 import BeautifulSoup


def get_types(text):
    bs = BeautifulSoup(text, 'html.parser')
    product_items = bs.find_all("div", {"class": "product-item"})
    types = []
    for item in product_items:
        ul = item.find('ul')
        li_list = ul.find_all('li')
        types += list(map(lambda e: e['type'], li_list))
    return types


path = Path("./2")
files = list(path.iterdir())

types = []

for file in files:
    print(file)
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        types += get_types(text)

s = set(types)
print(s)