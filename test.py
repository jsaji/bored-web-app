from bored_app.models import Activity, UserActivity
from flask import request, jsonify
import requests
'''
class User():
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email

    def something(self):
        print(self.name)

data = {'name':'jj', 'uid':5, 'email':'jj@g.com'}

user = User(**data)

print(user.name)
print(user.uid)
print(user.email)'''


def map_activity_model(activity_data):
    return {
        'description': activity_data['activity'],
        'activity_type':  activity_data['type'],
        'participants':  activity_data['participants'],
        'accessibility':  activity_data['accessibility'],
        'price':  activity_data['price'],
        'link': activity_data['link'],
        'random': 'yeet'
    }

r = requests.get('https://www.boredapi.com/api/activity')
raw_activity = map_activity_model(r.json())

activity = UserActivity(10, 10)
print(activity.user_activity_id)