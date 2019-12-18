import shelve

FILENAME = 'test_db'

# with shelve.open(FILENAME) as db:
#     db['new_key'] = 'New value'
#     db['new_key1'] = ['New value', 'new value 2']
#     db['new_key2'] = ['New value 3', 'new value 4']
#
# with shelve.open(FILENAME) as db:
#     for item in db.items():
#         print(item)


class UserDB:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename):
        self._filename = filename

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


db = UserDB(FILENAME)

db.create_user(**{'login': 'password'})
db.create_user(**{'login1': 'password1'})
print(db.get_all_users())