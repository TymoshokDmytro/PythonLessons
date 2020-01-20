def print_row(*args):
    print((("|   %-15s" * (len(args))) + "|") % args)


def fill_row(char, length):
    print(char * length)


def showResult(result, headers=None, length=80):
    print()
    if headers:
        print_row(*headers)
        fill_row('-', length)
    for res in result:
        print_row(*res)

