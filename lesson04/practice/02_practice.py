"""
Simple Dumb Social network
"""

import re
import traceback
from datetime import datetime
from enum import Enum, unique
import shelve

from lesson04.practice.utils import *

log = create_log('Exception_log.log')

@unique
class Role(Enum):
    ADMIN = 0
    USER = 1

class UserDB:

    def __init__(self, filename):
        self._filename = filename
        if not self.get_all_users():
            self.create_user({'root': User('root', '123', Role.ADMIN)})

    def get_db(self):
        return shelve.open(self._filename)

    def create_user(self, **kwargs):
        with shelve.open(self._filename) as db:
            users = db.get('users')

            if not users:
                db['users'] = kwargs
            else:
                users.update(kwargs)
                db['users'] = users

    def get_all_users(self):
        with shelve.open(self._filename) as db:
            return dict(db['users'].items())


class SocialNetworkException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class SocialNetwork:

    def __init__(self, name):
        self._name = name
        self._user_db = UserDB(name)
        self._users = {
            # пароль такой для прототы тестов
            # при регистрации нового пользователя пароль проверяется на валидность
            'root': User('root', '123', Role.ADMIN)
        }
        self._users.update(self._user_db.get_all_users())
        self._posts = [
            Post(0, "First root"),
            Post(0, "Second root"),
            Post(0, "First root"),
            Post(1, "First user"),
            Post(1, "Second user"),
            Post(1, "First user"),

        ]
        self._current_user = None
        self._current_role = None

    def set_current_user(self, user):
        self._current_user = user
        self._current_role = user.get_role()
        print('Current user set to [' + user.get_login() + ']')

    def get_current_user(self):
        return self._current_user

    def clear_current_user(self):
        self._current_user = None
        self._current_role = None
        print('Current user is None')

    def add_user(self, user):
        self._users.update({user.get_login(): user})

    def remove_user(self, id):
        for post in self._posts:
            if post.get_user_id() == id:
                self._posts.remove(post)
        user = self.get_user_by_id(id)
        self._users.pop(user)

    def check_user_authorized(func):
        def wrapper(self, *args):
            if self._current_user is None:
                raise SocialNetworkException('User is not authorized')
            return func(self, *args)
        return wrapper

    def check_admin(func):
        def wrapper(self, *args):
            if self._current_role is not Role.ADMIN:
                raise SocialNetworkException("This function is allowed only for ADMINS")
            return func(self, *args)
        return wrapper

    @check_user_authorized
    def create_post(self, message):
        self._posts.append(Post(self._current_user.get_id(), message))

    def remove_post(self, message):
        #TODO
        pass

    def is_login_present(self, login):
        return login in self._users.keys()

    def print_users(self):
        print_list(self._users.values())
        print()

    def print_posts(self, user_id=None):
        if user_id:
            print_list(self.get_posts_by_user_id(user_id))
        else:
            print_list(self._posts)

    def get_users(self):
        return self._users

    def get_ids(self):
        return [user.get_id() for user in self._users.values()]

    def get_user_by_id(self, user_id):
        if user_id not in self.get_ids():
            raise SocialNetworkException("This user is absent in users list")

        for user in self._users.values():
            if user.get_id() == user_id:
                return user
        raise SocialNetworkException(f"User with id [{user_id}] not found")

    def get_user_by_name(self, name):
        if name not in self._users.keys():
            raise SocialNetworkException(f"User with name {name} is absent in users list")
        return self._users.get(name)

    def get_user(self, login, password):
        if not self.is_login_present(login):
            raise SocialNetworkException(f"Login [{login}] not found")

        user = self._users.get(login)

        if password != base64decode(user.get_password()):
            raise SocialNetworkException("Invalid password")

        return user

    def get_posts(self):
        return self._posts

    def get_posts_by_user_id(self, user_id):
        return [post for post in self._posts if post.get_user_id() == user_id]

    def get_posts_by_user_name(self, user_name):
        user_id = self.get_user_by_name(user_name).get_id()
        return [post for post in self._posts if post.get_user_id() == user_id]

    def get_user_id_map(self):
        return {user.get_id(): user.get_login() for user in self._users.values()}

    def _show_posts(self, posts):
        user_id_map = self.get_user_id_map()
        if self._current_role == Role.ADMIN:
            for post in posts:
                print(f'Post_id: {post.get_id()}; Author: {user_id_map[post.get_user_id()]}; Message: {post.get_message()}; Created: {post.get_create_date()}')
        else:
            if not posts:
                print('No posts yet here :(')
                return
            for post in posts:
                print(f'Author: {user_id_map[post.get_user_id()]}; Message: {post.get_message()};')

    def show_all_posts(self):
        self._show_posts(self._posts)

    @check_admin
    def show_user_posts(self, name):
        posts = self.get_posts_by_user_name(name)
        self._show_posts(posts)

    @check_admin
    def show_all_users(self):
        for user in self._users.values():
            print(f'User_id: {user.get_id()}; Login(name): {user.get_login()}; Role: {user.get_role()}; Created: {user.get_registration_date()}')

    @check_admin
    def show_user_details_by_name(self, name):
        user = self.get_user_by_name(name)
        print(f'User_id: {user.get_id()}; Login(name): {user.get_login()}; Role: {user.get_role()}; Created: {user.get_registration_date()}')

    @check_admin
    def show_user_details_by_id(self, user_id):
        user = self.get_user_by_id(user_id)
        print(f'User_id: {user.get_id()}; Login(name): {user.get_login()}; Role: {user.get_role()}; Created: {user.get_registration_date()}')

class Registration:

    def __init__(self, social_network):
        self._social_network = social_network

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise SocialNetworkException("Make sure your password is at lest 8 letters")
        elif re.search('[0-9]', password) is None:
            raise SocialNetworkException("Make sure your password has a number in it")
        elif re.search('[A-Z]', password) is None:
            raise SocialNetworkException("Make sure your password has a capital letter in it")
        return True

    def register_user(self, login, password):
        if login == 'exit':
            raise SocialNetworkException('Do not use registered keywords as a login')
        if self._social_network.is_login_present(login):
            raise SocialNetworkException(f"Your login [{login}] is already present")

        self.validate_password(password)

        user = User(login, password, Role.USER)
        self._social_network.add_user(user)


class Authorization(Registration):

    def __init__(self, social_network):
        super(Authorization, self).__init__(social_network)

    def authorize_user(self, login, password):
        user = self._social_network.get_user(login, password)

        self._social_network.set_current_user(user)


class User:

    _id = 0

    def __init__(self, login, password, role):
        self._id = User._id
        User._id += 1
        if type(role) != Role:
            raise SocialNetworkException('Role must be of ROLE type')
        self._role = role
        self._login = login
        self._password = base64encode(password)
        self._registered = datetime.now()

    def __str__(self):
        return f'User[id={self._id} login={self._login}, role={self._role}]'

    def get_id(self):
        return self._id

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
        return f'Post[id={self._id}, user_id={self._user_id}, message={self._message}]'

    def get_message(self):
        return self._message

    def get_create_date(self):
        return self._created

    def get_user_id(self):
        return self._user_id

    def get_id(self):
        return self._id


sn = SocialNetwork("socialNetwork")
auth = Authorization(sn)


def get_input(promt):
    try:
        return int(input(promt))
    except ValueError:
        raise SocialNetworkException("Option must be of integer type")

print()
print('###### Welcome to the simple social network ######')
try:
    # unauthorized block
    while True:
        print()
        print("Please choose option: ")
        print("1 = Authorize")
        print("2 = Register")
        print("3 = Exit")
        try:
            opt = get_input("Choose option: ")
            # Authorization block
            if opt == 1:
                while True:
                    print()
                    print("Please enter creds or type 'exit' to go back: ")
                    login = input("Login: ")
                    if login == 'exit': break
                    password = input("Password: ")
                    try:
                        auth.authorize_user(login, password)
                        # if ok - proceed to messages block
                        print(f"You are in as {sn.get_current_user()}")
                        while True:
                            print()
                            print("1 = Show all posts")
                            print("2 = Create post")
                            print("3 = Show All users (ADMIN)")
                            print("4 = Show user details by name (ADMIN)")
                            print("5 = Show user details by id (ADMIN)")
                            print("6 = Show user posts by name (ADMIN)")
                            print("7 = Log out ")
                            try:
                                opt = get_input("Choose option: ")
                                if opt == 1:
                                    print('All posts: ')
                                    sn.show_all_posts()
                                elif opt == 2:
                                    message = input("Enter message:")
                                    sn.create_post(message)
                                    print('Your post successfully added')
                                elif opt == 3:
                                    sn.show_all_users()
                                elif opt == 4:
                                    user_name = input("Enter user name:")
                                    sn.show_user_details_by_name(user_name)
                                elif opt == 5:
                                    user_id = get_input("Enter user id: ")
                                    sn.show_user_details_by_id(user_id)
                                elif opt == 6:
                                    user_name = input("Enter user name: ")
                                    sn.show_user_posts(user_name)
                                elif opt == 7:
                                    sn.clear_current_user()
                                    print('Logged out')
                                    break
                                continue
                            except SocialNetworkException as e:
                                print("Error: ", e.args[0])
                                continue
                    except SocialNetworkException as e:
                        print("Error: ", e.args[0])
                        continue
            if opt == 2:
                while True:
                    print()
                    print("Please enter creds or type 'exit' to go back: ")
                    login = input("Login: ")
                    if login == 'exit': break
                    password = input("Password: ")
                    try:
                        auth.register_user(login, password)
                        print(f"User [{login}] successfully registered!")
                        break
                    except SocialNetworkException as e:
                        print("Error: ", e.args[0])
                        continue
            if opt == 3:
                break
        except SocialNetworkException as e:
            print("Error: ", e.args[0])
            continue
except Exception:
    log.error(traceback.format_exc())
    traceback.print_exc()

print('##### BYE #####')

