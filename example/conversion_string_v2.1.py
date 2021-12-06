"""
>> 'aaa-bbb-ccc[1-2].ya.ru tcp any'
...
'aaa-bbb-ccc1.ya.ru tcp any'
'aaa-bbb-ccc2.ya.ru tcp any'
...
"""


def _output_string(line, index_list, numbers_list, ports_list):
    line = line.split()
    url = line[0]
    if len(numbers_list) == 1:
        for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
            hostname = (f'{url[:index_list[0][0]]}'
                        f'{i}'
                        f'{url[index_list[0][1] + 1:]}')
            print(hostname)

    elif len(numbers_list) == 2:
        for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
            for y in range(numbers_list[1][0], numbers_list[1][1] + 1):
                hostname = f'{url[:index_list[0][0]]}'\
                           f'{i}'\
                           f'{url[index_list[0][1] + 1:index_list[1][0]]}'\
                           f'{y}'\
                           f'{url[index_list[1][1] + 1:]}'
                print(hostname)
    else:
        print('Не предусмотренная строка')


def conversion_string(line):
    index_list = list(zip([i for i in range(len(line)) if line[i] == '['],
                          [i for i in range(len(line)) if line[i] == ']']))

    ports_list = line.split()[2:]
    for i, value in enumerate(ports_list):
        ports_list[i] = value.replace(',', '')
        ports_list[i] = ports_list[i].replace('-', ' ')
    numbers_list = []
    for i in index_list:
        numbers = line[i[0]:i[1]]
        for y in range(len(numbers)):
            if not numbers[y].isdigit():
                numbers = numbers.replace(numbers[y], ' ')
        numbers_list.append(list(map(int, numbers.split())))

    _output_string(line, index_list, numbers_list, ports_list)


tmp = 'aaa-bbb-ccc[1-16].ya.ru tcp any'

LEFT_COMMAND = f'permit {tmp.split()[1]} any host'

conversion_string(tmp)
