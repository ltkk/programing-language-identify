import json


def load_json_file(path):
    return json.load(open(path, encoding='utf8'))


def save_list_to_file(datas, path):
    with open(path, 'w', encoding='utf8') as fp:
        for data in datas:
            fp.write(data + '\n')
