import random
import secrets
import string
from enum import unique, Enum


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


def generate_string(length, start_length_range=0, str_generate_type=string.ascii_letters):
    return ''.join(secrets.choice(str_generate_type) for i in
                   range((length if start_length_range == 0 else int(random.uniform(start_length_range, length)))))


def generate_int_length(length, start_length_range=0):
    return int(''.join(secrets.choice(string.digits) for i in
                       range((length if start_length_range == 0 else int(random.uniform(start_length_range, length))))))


def generate_random_int(max_value, start_length_range=0):
    return round(random.uniform(start_length_range, max_value))


def generate_random_float(max_value, start_length_range=0, round_value=0):
    return round(random.uniform(start_length_range, max_value), round_value)
