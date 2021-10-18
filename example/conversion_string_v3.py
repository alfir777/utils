import socket

"""
>>> 'ns[1-10].yandex.ru tcp 80, 85-90'
...
permit tcp any host 213.180.204.242 80
permit tcp any host 213.180.193.1 range 85 90
...
"""


def _output_string(line, index_list, numbers_list, ports_list):
    line = line.split()
    url = line[0]
    if len(numbers_list) == 1:
        for ports in ports_list:
            operator = ('eq' if ports.find('-') == -1 else 'range')
            ports = ports.replace('-', ' ')
            for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                hostname = (f'{url[:index_list[0][0]]}'
                            f'{i}'
                            f'{url[index_list[0][1] + 1:]}')
                hostname_ip = socket.gethostbyname(hostname)
                print(f'{LEFT_COMMAND} {hostname_ip} {operator} {ports}')

    elif len(numbers_list) == 2:
        for ports in ports_list:
            operator = ('eq' if ports.find('-') == -1 else 'range')
            ports = ports.replace('-', ' ')
            for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                for y in range(numbers_list[1][0], numbers_list[1][1] + 1):
                    hostname = f'{url[:index_list[0][0]]}'\
                               f'{i}'\
                               f'{url[index_list[0][1] + 1:index_list[1][0]]}'\
                               f'{y}'\
                               f'{url[index_list[1][1] + 1:]}'
                    hostname_ip = socket.gethostbyname(hostname)
                    print(f'{LEFT_COMMAND} {hostname_ip} {operator} {ports}')
    else:
        print('Не предусмотренная строка')


def conversion_string(line):
    index_list = list(zip([i for i in range(len(line)) if line[i] == '['],
                          [i for i in range(len(line)) if line[i] == ']']))

    ports_list = line.split()[2:]
    for i, value in enumerate(ports_list):
        if value.find(', '):
            ports_list[i] = value.replace(',', '')

    numbers_list = []
    for i in index_list:
        numbers = line[i[0]:i[1]]
        for y in range(len(numbers)):
            if not numbers[y].isdigit():
                numbers = numbers.replace(numbers[y], ' ')
        numbers_list.append(list(map(int, numbers.split())))

    _output_string(line, index_list, numbers_list, ports_list)


LEFT_COMMAND = 'permit tcp any host'

tmp = 'ns[5-10].yandex.ru tcp 80, 85-90'

conversion_string(tmp)
