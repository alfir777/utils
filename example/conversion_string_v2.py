# на входе test-[1-100]-asdasda.dasda.sdsda
# на выходе список:
# test-1-asdasda.dasda.sdsda
# test-2-asdasda.dasda.sdsda
# ..
# test-100-asdasda.dasda.sdsda

# часть 2
# tmp = 'aa-bb-ccc-ddddddd-[1:5].ee.xx.ff'
# tmp = 'aa-bb-[1-15]-ccc-ddddddd-[1:5].ee.xx.ff'
#
# часть 3
# aa-bb-cc.dd - это url
# поступает строка aa-[1-3]-bb.cc-dd-[1-2].gg.ru tcp 80, 85-90
# делаем из нее список
#
# aa-1-bb.cc-dd-1.gg.ru tcp 80
# aa-1-bb.cc-dd-1.gg.ru tcp 85-90


def output_string(line, index_list, numbers_list, ports_list):
    line = line.split()
    url = line[0]
    if len(numbers_list) == 1:
        for ports in ports_list:
            if ports.find('-') == -1:
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    print(f'permit tcp any host '
                          f'{url[:index_list[0][0]]}'
                          f'{i}'
                          f'{url[index_list[0][1] + 1:]}'
                          f' {ports}'
                          )
            else:
                ports = ports.replace('-', ' ')
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    print(f'permit tcp any host '
                          f'{url[:index_list[0][0]]}'
                          f'{i}'
                          f'{url[index_list[0][1] + 1:]}'
                          f' range {ports}'
                          )
    elif len(numbers_list) == 2:
        for ports in ports_list:
            if ports.find('-') == -1:
                for i in range(numbers_list[0][0], numbers_list[0][1]+1):
                    for y in range(numbers_list[1][0], numbers_list[1][1]+1):
                        print(f'permit tcp any host '
                              f'{url[:index_list[0][0]]}'
                              f'{i}'
                              f'{url[index_list[0][1] + 1:index_list[1][0]]}'
                              f'{y}'
                              f'{url[index_list[1][1] + 1:]}'
                              f' {ports}'
                              )
            else:
                ports = ports.replace('-', ' ')
                for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
                    for y in range(numbers_list[1][0], numbers_list[1][1] + 1):
                        print(f'permit tcp any host '
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

    line_list = line.split()
    ports_list = []
    for i, value in enumerate(line_list):
        if value in PROTOCOL_LIST:
            ports_list = line_list[i + 1:]
            break
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


PROTOCOL_LIST = ['tcp', 'udp']

# tmp = input()
# tmp = 'test-[1-100]-asdasda.dasda.sdsda'
# tmp = 'aa-bb-ccc-ddddddd-[1:5].ee.xx.ff'
# tmp = 'aa-bb-[1-15]-ccc-ddddddd-[1:5].ee.xx.ff'
tmp = 'aa-[1-4]-bb.cc.[1:5].gg.ru tcp 80, 85-90'

conversion_string(tmp)
