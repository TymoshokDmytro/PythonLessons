import base64
import logging
import os


def base64encode(string):
    return str(base64.b64encode(string.encode('utf-8', 'strict')), 'utf-8')


def base64decode(string):
    return str(base64.b64decode(string.encode('utf-8', 'strict')), 'utf-8')


def print_list(lst):
    for l in lst:
        print(l)

def create_log(log_file_name):
    if os.path.exists(log_file_name):
        os.remove(log_file_name)
    logging.basicConfig(filename=log_file_name, format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
    return logging

