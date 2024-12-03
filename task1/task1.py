from pathlib import Path
import json
from bs4 import BeautifulSoup
import pandas as pd


def parse_category(text):
    splitted = text.strip().split(' ')[1:]
    return ' '.join(splitted)


def parse_pages(text):
    return int(text.strip().split(' ')[1])


def parse_year(text):
    return int(text.strip().split(' ')[2])


def parse_isbn(text):
    return text.strip().split(':')[1]


def parse_description(text):
    return text.strip()[8:].strip()


def parse_rating(text):
    return float(text.strip().split(' ')[1])


def parse_watches(text):
    return int(text.strip().split(' ')[1])


def html_to_dict(file_name):
    result = {}

    with open(f'{file_name}', 'r', encoding='utf-8') as f:
        text = f.read()
    soup = BeautifulSoup(text, "html.parser")
    book_wrapper = soup.find_all("div", {"class": "book-wrapper"})[0]
    divs = book_wrapper.find_all("div")

    result['category'] = parse_category(divs[0].find('span').text)
    result['title'] = divs[1].find('h1').text.strip()
    result['author'] = divs[1].find('p').text.strip()

    spans = divs[2].find_all('span')
    result['pages'] = parse_pages(spans[0].text)
    result['publication_year'] = parse_year(spans[1].text)
    result['ISBN'] = parse_isbn(spans[2].text)

    result['description'] = parse_description(divs[2].find('p').text)

    spans = divs[4].find_all('span')
    result['rating'] = parse_rating(spans[0].text)
    result['watches'] = parse_watches(spans[1].text)

    return result

path = Path("./1")
files = list(path.iterdir())

dicts = []
for file_path in files:
    print(file_path)
    dicts.append(html_to_dict(file_path))

with open('../outputs/task1/task1.json', 'w', encoding='utf-8') as output_file:
    json.dump(dicts, output_file, indent=4, ensure_ascii=False)

df = pd.read_json('../outputs/task1/task1.json')
df = df.sort_values('category')
df.to_csv('../outputs/task1/sorted.csv')

filtered_df = df[df['author'] == 'Майн Рид']
filtered_df.to_csv('../outputs/task1/filtered.csv')

stats = df['pages'].describe().to_dict()
with open('../outputs/task1/pages_stats.json', 'w', encoding='utf-8') as output_file:
    json.dump(stats, output_file, indent=4, ensure_ascii=False)

freqs = df['description'].value_counts().to_dict()
with open('../outputs/task1/description_freqs.json', 'w', encoding='utf-8') as output_file:
    json.dump(freqs, output_file, indent=4, ensure_ascii=False)
