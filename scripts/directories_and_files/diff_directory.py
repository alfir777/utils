import ast
import json
import os
import jsondiff


def get_directory(user_input=1):
    path = input('Введите путь для сравнения')
    if not os.path.exists(path):
        exit('Указанного пути не существует')
    report_ff = ''
    if user_input == 1:
        report_ff = 'report_initial.json'
    elif user_input == 2:
        report_ff = 'report_for_diff.json'

    res = dict()
    for root, dirs, files in os.walk(path):
        for item in files:
            if os.name == 'nt':
                root_list = os.path.join(root, item).split('\\')
            else:
                root_list = os.path.join(root, item).split('/')
            d = res
            for i in root_list:
                d = d.setdefault(i, dict())
    json_data = json.dumps(res, indent=4, sort_keys=True, ensure_ascii=False)

    with open(report_ff, 'w+', encoding='utf-8') as ff:
        ff.write(json_data)


def diff_directory():
    with open('report_initial.json', 'r', encoding='utf-8') as ff1:
        with open('report_for_diff.json', 'r', encoding='utf-8') as ff2:
            json_data1 = ff1.read()
            json_data2 = ff2.read()
            jsondiff_data = jsondiff.diff(json_data1, json_data2, load=True, dump=True)
    json_data = json.dumps(ast.literal_eval(jsondiff_data), indent=4, sort_keys=True, ensure_ascii=False)
    with open('diff_report.json', 'w+', encoding='utf-8') as ff:
        ff.write(json_data)


def main():
    user_input = input('1. Сформировать начальный файл\n'
                       '2. Сформировать файл сравнения\n'
                       '3. Сравнить два файла\n')
    if user_input == '1':
        get_directory(user_input=1)
    elif user_input == '2':
        get_directory(user_input=2)
    elif user_input == '3':
        if not os.path.exists('report_initial.json'):
            exit('Нет начального файла')
        if not os.path.exists('report_for_diff.json'):
            exit('Нет файла для сравнения')
        diff_directory()
    else:
        exit('Ничего не выбрано')


if __name__ == '__main__':
    main()
