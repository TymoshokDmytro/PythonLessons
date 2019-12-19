from datetime import datetime
from enum import Enum, unique
from lesson04.practice.utils import *


@unique
class Role(Enum):
    ADMIN = 0
    USER = 1


class SocialNetwork:

    def __init__(self):
        self._users = [
            User('root', 'calvin', Role.ADMIN),
            User('user1', '123', Role.USER),
        ]
        self._posts = []
        self._current_user = None

    def print_users(self):
        print_list(self._users)

    def print_posts(self):
        print_list(self._posts)

    def get_users(self):
        return self._users

    def get_posts(self):
        return self._posts


class Registration:

    def __init__(self, social_network):
        self._social_network = social_network

    def set_social_network(self, social_network):
        self._social_network = social_network

    def is_login_present(self, login):
        return login in [user.get_login() for user in self._social_network.get_users()]


class Authorization(Registration):

    def __init__(self, social_network):
        super(Authorization, self).__init__(social_network)
        
    def set_social_network(self, social_network):
        super(Authorization, self).set_social_network(social_network)
        

class User:

    _id = 0

    def __init__(self, login, password, role):
        self._id = User._id
        User._id += 1
        if type(role) != Role:
            raise Exception('Role must be of ROLE type')
        self._role = role
        self._login = login
        self._password = base64encode(password)
        self._registered = datetime.now()

    def __str__(self):
        return f'User[login={self._login}, role={self._role}]'

    def get_registration_date(self):
        return self._registered

    def get_login(self):
        return self._login

    def get_password(self):
        return self._password

    def get_role(self):
        return self._role


class Post:

    _id = 0

    def __init__(self, user_id, message):
        self._id = Post._id
        Post._id += 1
        self._user_id = user_id
        self._message = message
        self._created = datetime.now()

    def __str__(self):
        return f'Post[login={self._message}]'

    def get_message(self):
        return self._message

    def get_create_date(self):
        return self._created

    def user_id(self):
        return self._user_id


sn = SocialNetwork()
registration = Registration(sn)


sn.print_users()
sn.print_posts()


