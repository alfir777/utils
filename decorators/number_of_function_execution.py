count = 0


def number_of_function_execution(func):
    def surrogate(*args, **kwargs):
        global count
        count += 1
        result = func(*args, **kwargs)
        return result

    return surrogate


@number_of_function_execution
def main():
    print('hello')


main()
main()
main()
main()

print(count)
