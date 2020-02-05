from enum import Enum, unique
from pprint import pprint

from mongoengine import *

connect('bot_consulting_db', alias='bot_consulting_db')


@unique
class STATE(Enum):
    PHONE = 'phone'
    PHONE_ENTERING = 'phone_entering'
    EMAIL = 'email'
    EMAIL_ENTERING = 'email_entering'
    ADDRESS = 'address'
    ADDRESS_ENTERING = 'address_entering'
    REGISTERED = 'registered'


states = ['phone', 'phone_entering', 'email', 'email_entering', 'address',  'address_entering', 'registered']
state_order = {state: i + 1 for i, state in enumerate(states)}
state_choices = set((state, state) for state in states)


class User(Document):
    telegram_id = StringField(max_length=32, required=True)
    username = StringField(max_length=128)
    fullname = StringField(max_length=256)
    phone = StringField(max_length=20)
    email = EmailField()
    state = StringField(choices=state_choices, default=states[0])


class Complient(Document):
    creation_date = DateField()
    description = StringField(max_length=4096)
    user = ReferenceField(User)


if __name__ == '__main__':
    pass
    User.drop_collection()
