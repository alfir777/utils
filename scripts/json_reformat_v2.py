import ast
import json
import os


def json_reformat(input_file, indent=4, sort_keys=True):
    res = []
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf8') as file:
            for line in file:
                try:
                    data = ast.literal_eval(line)
                except SyntaxError as exс:
                    print(f'ошибка в строке: {line}')
                if data["deleted"]:
                    res.append(data)
        json_data = json.dumps(res, indent=indent, sort_keys=sort_keys)
        with open('report.json', 'w+', encoding='utf8') as file:
            file.write(json_data)
    else:
        print('File not found')


file_json = '1.txt'
json_reformat(file_json, indent=4, sort_keys=False)
