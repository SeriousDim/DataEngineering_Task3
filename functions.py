import json


def dicts_to_json(dicts, save_as):
    with open(save_as, 'w', encoding='utf-8') as output_file:
        json.dump(dicts, output_file, indent=4, ensure_ascii=False)


def sort_df(df, field, save_as):
    result_df = df.sort_values(field)
    if save_as:
        result_df.to_csv(save_as)
    return result_df


def filter_df(df, field, value, save_as):
    result_df = df[df[field] == value]
    if save_as:
        result_df.to_csv(save_as)
    return result_df


def get_statistics(df, field, save_as):
    stats = df[field].describe().to_dict()
    if save_as:
        with open(save_as, 'w', encoding='utf-8') as output_file:
            json.dump(stats, output_file, indent=4, ensure_ascii=False)
    return stats


def get_frequencies(df, field, save_as):
    stats = df[field].value_counts().to_dict()
    if save_as:
        with open(save_as, 'w', encoding='utf-8') as output_file:
            json.dump(stats, output_file, indent=4, ensure_ascii=False)
    return stats
