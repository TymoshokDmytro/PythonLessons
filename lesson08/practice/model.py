import os
from enum import unique, Enum

from werkzeug.utils import redirect

from lesson07.practice.DBManager import DBManager


@unique
class Role(Enum):
    USER = 1,
    ADMIN = 2


class OnlineStoreDBService:
    def __init__(self, db_path, autocommit):
        if not os.path.exists(db_path):
            raise Exception('DB not found on this path: ' + db_path)
        self._db_manager = DBManager(db_path, autocommit)


class OnlineStore:
    def __init__(self, db_service, auth):
        self.db_service = db_service


class AuthenticationService(object):
    _user = None
    _role = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AuthenticationService, cls).__new__(cls)
        return cls.instance

    # Predefined users
    _users = {
        'user': {
            'password': 'user',
            'role': Role.USER
        },
        'root': {
            'password': 'root',
            'role': Role.ADMIN
        }
    }

    @classmethod
    def get_role(cls):
        return cls._role

    @classmethod
    def get_user(cls):
        return cls._user

    @classmethod
    def login(cls, login, password):
        if (not login) or (not password):
            return {'error': 'Fields cannot be empty '}
        if login and login not in cls._users.keys():
            return {'error': 'No such user '}
        user = cls._users[login]
        if password and password != user['password']:
            return {'error': 'Incorrect password'}

        cls._user = login
        cls._role = user['role']
        return {'status': 'ok'}

    @classmethod
    def check_user_exists(cls, login):
        if login not in cls._users.keys():
            return False
        return True

    @classmethod
    def is_authenticated(cls):
        if cls._user is None:
            return False
        return True

    @classmethod
    def logout(cls):
        cls._user = None
        cls._role = None


def check_auth(func):
    def wrapper_1(*args, **kwargs):
        if not AuthenticationService.is_authenticated():
            # return render_template('login.html', error_message='User not authenticated')
            return redirect('login')
        return func(*args, **kwargs)

    return wrapper_1


def only_for_role(role):
    return only_for_roles([role])


def only_for_roles(roles):
    def decorator(func):
        def wrapper_2(*args, **kwargs):
            if not AuthenticationService.is_authenticated():
                redirect('login')
            if not AuthenticationService.get_role() in roles:
                from werkzeug.exceptions import abort
                abort(405)
            return func(*args, **kwargs)

        return wrapper_2

    return decorator