import json

users = {
    'user1': 'authenticated',
    'user2': 'authorized',
    'user3': 'anon'
}

json_obj = json.dumps(users, indent=3)
result = json_obj
print(json_obj)
