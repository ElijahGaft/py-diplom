import json
import sys
import time
from urllib.parse import urlencode
import requests
from pip._vendor.msgpack.fallback import xrange

APP_ID = 7058177  # ID моего приложения зарегестрированного на сайте VK
AUTH_URL = 'https://oauth.vk.com/authorize'
Auth_DATA = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'groups, friends',
    'response_type': 'token'
}
# print('?'.join((AUTH_URL, urlencode(Auth_DATA)))) # выдаёт ссылку на страничку разрешений прав, так я могу узнать токен.

TOKEN = 'e3638c6fe52a3ff7f69739650044b91136a8d2d8106c2add2b6282411215a04584a591184d981b9db7b4b'  # токен моего пользователя через которого идут все запросы


class User:
    def __init__(self, user_id, token):  # При создании обьекта класса, мы должны передать имя или ID пользователя
        self.user_id = user_id
        self.token = token

    def get_params(self):
        return {
            'access_token': self.token,
            'v': '5.25',
            'user_id': self.user_id
        }

    def request(self, method, params):  # Формирование запроса
        response = requests.get(
            'https://api.vk.com/method/' + method,
            params=params
        )
        return response

    def get_friends(self):
        params = self.get_params()
        response = self.request(
            'friends.get',
            params=params
        )
        return response.json()['response']

    def get_groups(self):
        params = self.get_params()
        response = self.request(
            'groups.get',
            params=params
        )
        return response.json()['response']


def user_group_analise(id):
    try:
        FRIEND = User(id, TOKEN)
        user_group = FRIEND.get_groups()
        user_group = user_group.get('items')
        return user_group
    except:
        pass


def same_group(user1_list, user2_list):
    try:
        set(user2_list).difference(set(user1_list))
        return user2_list
    except:
        pass

if __name__ == '__main__':
    Evgeniy = User('171691064', TOKEN)
    friends = Evgeniy.get_friends()  # метод класса для поиска друзей юзера, переменная хранит словарь (имя и id)
    friends = friends.get('items')
    groups = Evgeniy.get_groups() # с помощью метода класса создаём список групп юзера
    print(groups)
    groups = groups.get('items')
    print(groups)
    counter = 0
    for user_id in friends:
        groups_list = user_group_analise(str(user_id))
        groups = same_group(groups_list, groups)
        sys.stdout.write('\r')
        part = float(counter) / len(friends)
        symbols_num = int(100 * part)
        sys.stdout.write("[%-100s] %3.2f%%" % ('=' * symbols_num, part * 100))
        sys.stdout.flush()
        time.sleep(0.01)
        counter += 1
    print(groups)

    with open('group.json', 'w' ) as f:
        data = {'gid': groups}
        json.dump(data, f, ensure_ascii = False, indent = 2)

