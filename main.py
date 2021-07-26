# -*- coding: utf-8 -*-

import json
import os
import time
import zipfile
from datetime import date
import smtplib
import config


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


def report_to_email():
    smtp_obj = smtplib.SMTP('smtp.yandex.ru', 465)
    smtp_obj.starttls()
    smtp_obj.login(config.sender_login, config.sender_password)
    smtp_obj.sendmail('admin@jatu.ru', 'test')


class MonitorFiles:
    """
    Сравнение файлов в директории с предыдущим выполнением
    :param src: целевая директория для сравнения
    """

    def __init__(self, src):
        if not os.path.isdir('temp'):
            os.mkdir('temp')
        if not os.path.isdir('reports'):
            os.mkdir('reports')
        if os.path.exists(src):
            self.src = os.path.normpath(src)
        else:
            print('Не указана начальная директория')
        self.report_file = 'reports\\report_' + str(date.today()) + str(time.time()) + '.txt'
        self.previous_report_file = ''
        self.json_report_file = 'report.json'
        self.diff_add = os.path.normpath('temp\\diff_add.txt')
        self.diff_dell = os.path.normpath('temp\\diff_del.txt')
        self.diff = {}

    def run(self):
        initial_scan = list(os.scandir('reports'))
        if len(initial_scan) == 0:
            self.scan()
            print('Первое сканирование директории')
        else:
            self.scan()
            self.compare()
            self.report_json()
            self.add_zip()

    def scan(self):
        with open(self.report_file, 'w', encoding='utf8') as ff:
            for dir_path, dir_names, filenames in os.walk(self.src):
                for file in filenames:
                    full_file_path = os.path.join(dir_path, file)
                    ff.write(f'{full_file_path}\n')

    def compare(self):
        file_list = os.listdir('reports')
        full_list = [os.path.join('reports', i) for i in file_list]
        time_sorted_list = sorted(full_list, key=os.path.getmtime)
        self.previous_report_file = time_sorted_list[-2]

        with open(self.report_file) as report_file:
            with open(self.previous_report_file) as report_old:
                with open(self.diff_add, 'w', encoding='utf8') as diff:
                    diff.writelines(set(report_file).difference(report_old))

        with open(self.report_file) as report_file:
            with open(self.previous_report_file) as report_old:
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
        with open(self.json_report_file, 'w', encoding='utf8') as file:
            file.write(json_data_sorted)

    def add_zip(self):
        with zipfile.ZipFile('report.zip', 'w') as file_zip:
            file_zip.write(self.json_report_file, compress_type=zipfile.ZIP_DEFLATED)


@time_track
def main(path):
    monitor_path = MonitorFiles(src=path)
    monitor_path.run()


if __name__ == '__main__':
    folder = 'C:\\Windows\\'
    main(path=folder)
