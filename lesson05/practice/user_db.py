import shelve

class UserDB:

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
            return dict(db)

db = UserDB('socialNetwork')

users = db.get_all_users()
print(users)
