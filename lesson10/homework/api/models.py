import datetime
import random
from pprint import pprint

from mongoengine import *
import lorem
from faker import Faker

connect('rest_homework_shop_db')


class RestShopDataGenerator:

    @staticmethod
    def generate_data(self):
        pass


if __name__ == '__main__':
    RestShopDataGenerator.generate_data()
