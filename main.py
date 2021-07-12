# -*- coding: utf-8 -*-

# Дано: каталог, в него периодически льются файлы.
# Может 1 файл, может папка. Так же файлы могут удалятся. И папки тоже.
# Надо: написать скрипт, который будет смотреть в целевую папку, при обнаружении изменений будет создаваться отчет.
# В отчете должна быть информация о файле, его размере, атрибутах, времени изменения.
# *1: отчет должен быть в формате json для чтения парсерами
import json
import os
import time
from datetime import date


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate


def scan_for_test(path):
    with open('report.txt', 'w+', encoding='utf8') as ff:
        for dir_path, dir_names, filenames in os.walk(path):
            for file in filenames:
                full_file_path = os.path.join(dir_path, file)
                ff.write(f'{full_file_path}\n')


class MonitorFiles:

    def __init__(self, src):
        if os.path.exists(path):
            self.src = os.path.normpath(src)
        else:
            print('Не указана начальная папка')
        self.report_file = ''
        self.diff_add = 'diff_add.txt'
        self.diff_dell = 'diff_del.txt'
        self.diff = {}

    def scan(self):
        current_date = date.today()
        self.report_file = 'report_' + str(current_date) + '.txt'
        with open(self.report_file, 'w+', encoding='utf8') as ff:
            for dir_path, dir_names, filenames in os.walk(self.src):
                for file in filenames:
                    full_file_path = os.path.join(dir_path, file)
                    ff.write(f'{full_file_path}\n')

    def compare(self):
        with open(self.report_file) as report_file:
            with open('report.txt') as report_old:
                with open(self.diff_add, 'w', encoding='utf8') as diff:
                    diff.writelines(set(report_file).difference(report_old))

        with open(self.report_file) as report_file:
            with open('report.txt') as report_old:
                with open(self.diff_dell, 'w', encoding='utf8') as diff:
                    diff.writelines(set(report_old).difference(report_file))

    def report_json(self):
        with open(self.diff_add, 'r', encoding='utf8') as diff:
            for line in diff:
                line = os.path.normpath(line.rstrip('\n'))
                file_name = os.path.basename(line)
                file_size = os.path.getsize(line)
                file_size_kb = str(file_size // 1024) + ' Kb'
                secs = os.path.getmtime(line)
                file_time = time.ctime(secs)
                self.diff[file_name] = ('add', line, file_size_kb, file_time)
        with open(self.diff_dell, 'r', encoding='utf8') as diff:
            for line in diff:
                line = os.path.normpath(line.rstrip('\n'))
                file_name = os.path.basename(line)
                self.diff[file_name] = ('DELETE', line)
        json_data_sorted = json.dumps(self.diff, indent=4, sort_keys=True)
        with open('report.json', 'w', encoding='utf8') as file:
            file.write(json_data_sorted)


@time_track
def main(path):
    monitor_path = MonitorFiles(src=path)
    monitor_path.scan()
    monitor_path.compare()
    monitor_path.report_json()


if __name__ == '__main__':
    path = 'C:\\Windows\\'
    # scan_for_test(path)   # необходима для первичного создания отчета для сравнения
    main(path)
