import socket


"""
>>> 'ns[1-10].yandex.ru tcp 80, 85-90'
...
permit tcp any host 213.180.204.242 80
permit tcp any host 213.180.193.1 range 85 90
...
"""


def output_string(line, index_list, numbers_list, ports_list):
    line = line.split()
    url = line[0]
    if len(numbers_list) == 1:
        for ports in ports_list:
            if ports.find('-') == -1:
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    hostname = (f'{url[:index_list[0][0]]}'
                                f'{i}'
                                f'{url[index_list[0][1] + 1:]}')
                    hostname_ip = socket.gethostbyname(hostname)
                    print(f'{LEFT_COMMAND}'
                          f'{hostname_ip}'
                          f' eq {ports}'
                          )
            else:
                ports = ports.replace('-', ' ')
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    hostname = (f'{url[:index_list[0][0]]}'
                                f'{i}'
                                f'{url[index_list[0][1] + 1:]}')
                    hostname_ip = socket.gethostbyname(hostname)
                    print(f'{LEFT_COMMAND}'
                          f'{hostname_ip}'
                          f' range {ports}'
                          )
    elif len(numbers_list) == 2:
        for ports in ports_list:
            if ports.find('-') == -1:
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    for y in range(numbers_list[1][0], numbers_list[1][1] + 1):
                        print(f'{LEFT_COMMAND}'
                              f'{url[:index_list[0][0]]}'
                              f'{i}'
                              f'{url[index_list[0][1] + 1:index_list[1][0]]}'
                              f'{y}'
                              f'{url[index_list[1][1] + 1:]}'
                              f' eq {ports}'
                              )
            else:
                ports = ports.replace('-', ' ')
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    for y in range(numbers_list[1][0], numbers_list[1][1] + 1):
                        print(f'{LEFT_COMMAND}'
                              f'{url[:index_list[0][0]]}'
                              f'{i}'
                              f'{url[index_list[0][1] + 1:index_list[1][0]]}'
                              f'{y}'
                              f'{url[index_list[1][1] + 1:]}'
                              f' range {ports}'
                              )
    else:
        print('Не предусмотренная строка')


def conversion_string(line):
    index_open = []
    index_close = []
    for i in range(len(line)):
        if line[i] == '[':
            index_open.append(i)
        if line[i] == ']':
            index_close.append(i)
    index_list = list(zip(index_open, index_close))

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

    output_string(line, index_list, numbers_list, ports_list)


LEFT_COMMAND = 'permit tcp any host '

tmp = 'ns[1-10].yandex.ru tcp 80, 85-90'

conversion_string(tmp)
