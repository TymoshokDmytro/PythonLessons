import base64


def base64encode(string):
    return str(base64.b64encode(string.encode('utf-8', 'strict')), 'utf-8')


def base64decode(string):
    return str(base64.b64decode(string.encode('utf-8', 'strict')), 'utf-8')


def print_list(lst):
    for l in lst:
        print(l)
