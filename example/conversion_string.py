# на входе test-[1-100]-asdasda.dasda.sdsda
# на выходе список:
# test-1-asdasda.dasda.sdsda
# test-2-asdasda.dasda.sdsda
# ..
# test-100-asdasda.dasda.sdsda


def output_string(line, index_list, numbers_list):

    if len(numbers_list) == 1:
        for i in range(numbers_list[0][0], numbers_list[0][1] + 1):
            print(f'{line[:index_list[0][0]]}-{i}-{line[index_list[0][1]+2:]}')
    elif len(numbers_list) == 2:
        for i in range(numbers_list[0][0], numbers_list[0][1]):
            for y in range(numbers_list[1][0], numbers_list[1][1]):
                print(f'{line[:index_list[0][0]]}'
                      f'{i}'
                      f'{line[index_list[0][1]+1:index_list[1][0]]}'
                      f'{y}'
                      f'{line[index_list[1][1]+1:]}')
    else:
        print('Не предусмотрено более двух')


def conversion_string(line):
    index_open = []
    index_close = []
    for i in range(len(line)):
        if line[i] == '[':
            index_open.append(i)
        if line[i] == ']':
            index_close.append(i)
    index_list = list(zip(index_open, index_close))

    numbers_list = []
    for i in index_list:
        numbers = line[i[0]:i[1]]
        for y in range(len(numbers)):
            if not numbers[y].isdigit():
                numbers = numbers.replace(numbers[y], ' ')
        numbers_list.append(list(map(int, numbers.split())))

    output_string(line, index_list, numbers_list)


# tmp = input()
# tmp = 'test-[1-100]-asdasda.dasda.sdsda'
# tmp = 'aa-bb-ccc-ddddddd-[1:5].ee.xx.ff'
tmp = 'aa-bb-[1-15]-ccc-ddddddd-[1:5].ee.xx.ff'

conversion_string(tmp)
