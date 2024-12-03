from bs4 import BeautifulSoup
import requests
import json


def parse_catalog_to_dict(text):
    result = []

    bs = BeautifulSoup(text, 'html.parser')
    news_block = bs.find('div', {'class': 'backgroundWhite px-4 pt-3 pb-0'})
    news = news_block.find('div').find_all('div', recursive=False)[1:21]

    for new in news:
        parsed_element = {}

        element = new.find('a')
        parsed_element['href'] = element['href']

        title_element = element.find('div', {'class': 'cardHeader'})
        parsed_element['title'] = title_element.text.strip()

        desc_element = element.find('div', {'class': 'cardSubheader'})
        parsed_element['desc'] = desc_element.text.strip()

        secondary_info = element.find('div', {'class': 'textTypeSecond'}).find_all('div', recursive=False)
        parsed_element['category'] = secondary_info[1].text.strip()

        result.append(parsed_element)

    return result


def parse_page_to_dict(text):
    result = {}

    bs = BeautifulSoup(text, 'html.parser')
    author = bs.find('div', {'class': 'pl-2 textTypeSecond blackLink'})
    result['author'] = author.text.strip()

    header = bs.find('h1', {'itemprop': 'headline'})
    result['header'] = header.text.strip()

    paragraphs = bs.find('div', {'itemprop': 'articleBody'})
    result['article_length'] = len(paragraphs.text.strip())

    return result


base_url = 'https://www.1obl.ru'
url = f'{base_url}/news/'
response = requests.get(url)
content = response.content

parsed_news = parse_catalog_to_dict(content)
with open('../outputs/task5/news.json', 'w', encoding='utf-8') as output_file:
    json.dump(parsed_news, output_file, indent=4, ensure_ascii=False)

articles = []
for new in parsed_news:
    url = f'{base_url}{new['href']}'
    response = requests.get(url)
    content = response.content
    articles.append(parse_page_to_dict(content))

with open('../outputs/task5/articles.json', 'w', encoding='utf-8') as output_file:
    json.dump(articles, output_file, indent=4, ensure_ascii=False)
