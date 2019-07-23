import sys
import progressbar
import time
from urllib.parse import urlencode
import requests
from pip._vendor.msgpack.fallback import xrange

APP_ID = 7058177     # ID моего приложения зарегестрированного на сайте VK
AUTH_URL = 'https://oauth.vk.com/authorize'
Auth_DATA = {
    'client_id' : APP_ID,
    'display' : 'page',
    'scope' : 'status',
    'response_type' : 'token'
}
# print('?'.join((AUTH_URL, urlencode(Auth_DATA)))) # выдаёт ссылку на страничку разрешений прав, так я могу узнать токен.

TOKEN = '91abd09a4e6e1053fe5453b683b48abb1dc97f75cfdcfa94c580b4c0493e20e023db92ac6adc0bc5cd8d8' # токен моего пользователя через которого идут все запросы

class User:
    def __init__(self,user_id, token): # При создании обьекта класса, мы должны передать имя или ID пользователя
        self.user_id = user_id
        self.token = token

    def get_params(self):
        return {
            'access_token' : self.token,
            'v' : '5.25',
            'user_id' : self.user_id
        }


    def request(self, method, params): # Формирование запроса
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

def User_group_analise(id):
    try:
        FRIEND = User(id, TOKEN)
        user_group = FRIEND.get_groups()
        user_group = user_group.get('items')
        print('.', end='')
        return user_group
    except:
        pass

def Same_group(user1_list, user2_list):
    try:
        set(user2_list).difference(set(user1_list))
    except:
        pass
    return user2_list


def show_progress(value):
    sys.stderr.write('%d\r' % value)

ILYA = User('171691064', TOKEN)
# с помощью метода класса создаём список групп юзера
friends = ILYA.get_friends() # метод класса для поиска друзей юзера, переменная хранит словарь (имя и id)
friends = friends.get('items')
groups = ILYA.get_groups()
groups = groups.get('items')
counter = 0
print(groups)
# for i in range(1, len(friends)):
#     sys.stdout.write('\r')
#     part = float(i)/(len(friends)-1)
#     symbols_num = int(100 * part)
#     sys.stdout.write("[%-100s] %3.2f%%" % ('='*symbols_num, part*100))
#     sys.stdout.flush()
#     time.sleep(0.01)
for user_id in friends:
    groups_list = User_group_analise(str(user_id))
    groups = Same_group(groups_list, groups)
    sys.stdout.write('\r')
    part = float(counter)/len(friends)
    symbols_num = int(100 * part)
    sys.stdout.write("[%-100s] %3.2f%%" % ('=' * symbols_num, part * 100))
    sys.stdout.flush()
    time.sleep(0.01)
    counter += 1
print('\n')
# для каждого друга применяем метод поиска груп, сравниваем с групами нашего юзера и удаляем из его списка, если находит повторения.
# ВОПРОС: Смогу ли я применять метод класа юзера на его друзьях, или сначала для каждого друга мне по id нужно создать свой обьект класса?
print(groups)