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

TOKEN = 'c92d44116b239b0f6b8484a6b864cb45602235e95d003bad3f4d3462352e90567a384511348de6b64ea89'  # токен моего пользователя через которого идут все запросы


class User:
    def __init__(self, user_id, token):  # При создании обьекта класса, мы должны передать имя или ID пользователя
        self.user_id = user_id
        self.token = token

    def get_params(self):
        return {
            'access_token': self.token,
            'v': '5.61',
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

    def group_info(self, id_gr):
        self.id_gr = id_gr
        params = {
            'access_token': self.token,
            'v': '5.61',
            'group_id': self.id_gr,
            'fields' : 'members_count'
        }
        time.sleep(3)
        response = self.request(
            'groups.getById',
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
        if user1_list == None:
            raise ImportError
        if user2_list == None:
            raise

        user2_list = set(user2_list)
        user1_list = set(user1_list)

        if user2_list.isdisjoint(user1_list) == False: #истина, если set и other не имеют общих элементов.
            print('ЕСТЬ пересечений с множеством')
            user2_list.difference_update(user1_list)
            print(list(user2_list))

    except ImportError :
        pass
    except :
        pass
    return list(user2_list)
if __name__ == '__main__':
    Evgeniy = User('171691064', TOKEN)
    friends = Evgeniy.get_friends()  # метод класса для поиска друзей юзера, переменная хранит словарь (имя и id)
    friends = friends.get('items')
    groups = Evgeniy.get_groups() # с помощью метода класса создаём список групп юзера

    groups = groups.get('items')
    counter = 0
    for us_id in friends:
        groups_list = user_group_analise(str(us_id))
        groups = same_group(groups_list, groups)
        sys.stdout.write('\r')
        part = float(counter) / len(friends)
        symbols_num = int(100 * part)
        sys.stdout.write("[%-100s] %3.2f%%" % ('=' * symbols_num, part * 100))
        sys.stdout.flush()
        time.sleep(0.01)
        counter += 1
    name_gr = []
    members_count_gr = []
    # print(groups, '0')
    for id in groups:
        group_info = Evgeniy.group_info(id)
        for info in group_info:
            name = info.get('name')
            name_gr.append(name)
            members_count = info.get('members_count')
            members_count_gr.append(members_count)

    # print(name_gr, '2')
    # print(members_count_gr, '3')
    len = len(groups)
    data_group = []
    while len != 0:
        gr_inf = {'name': name_gr[len - 1],
                  'gid': groups[len - 1],
                  'members_count': members_count_gr[len - 1]}
        data_group.append(gr_inf)
        len -= 1
    with open('group.json', 'w') as f:
        data = data_group
        json.dump(data, f, ensure_ascii = False, indent = 2)

