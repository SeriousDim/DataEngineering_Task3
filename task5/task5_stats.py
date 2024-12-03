import pandas as pd
from functions import dicts_to_json, sort_df, filter_df, get_statistics, get_frequencies

# Список новостей
df = pd.read_json('../outputs/task5/news.json')
output_path = '../outputs/task5/news'

sort_df(df, 'title', f'{output_path}/sorted.csv')

filtered_df = df[df['category'] == 'Спорт']
filtered_df.to_csv(f'{output_path}/filtered.csv')

get_frequencies(df, 'category', f'{output_path}/categories_freqs.json')

# Статьи
df = pd.read_json('../outputs/task5/articles.json')
output_path = '../outputs/task5/articles'

sort_df(df, 'article_length', f'{output_path}/sorted.csv')

filtered_df = df[df['author'] == 'Анастасия Посохова']
filtered_df.to_csv(f'{output_path}/filtered.csv')

get_statistics(df, 'article_length', f'{output_path}/length_stats.json')
get_frequencies(df, 'author', f'{output_path}/author_freqs.json')
