# Задание:
# Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей. В качестве жертвы, на ком тестировать, можно использовать: https://vk.com/eshmargunov
#
# Входные данные:
# Имя пользователя или его id в ВК, для которого мы проводим исследование.
#
# Внимание: и имя пользователя (eshmargunov) и id (171691064) - являются валидными входными данными.
#
# Ввод можно организовать любым способом:
#
# из консоли
# из параметров командной строки при запуске
# из переменной
# Выходные данные:
# Файл groups.json в формате:



from urllib.parse import urlencode
import requests

APP_ID = 7058177     # ID моего приложения зарегестрированного на сайте VK
AUTH_URL = 'https://oauth.vk.com/authorize'
Auth_DATA = {
    'client_id' : APP_ID,
    'display' : 'page',
    'scope' : 'status',
    'response_type' : 'token',
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
            'user_id' : self.user_id,
            'fields' : 'nickname'
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


Evgeniy = User(306008470, TOKEN)
# с помощью метода класса создаём список групп юзера
Friends = Evgeniy.get_friends()# метод класса для поиска друзей юзера, переменная хранит словарь (имя и id)
# для каждого друга применяем метод поиска груп, сравниваем с групами нашего юзера и удаляем из его списка, если находит повторения.
# ВОПРОС: Смогу ли я применять метод класа юзера на его друзьях, или сначала для каждого друга мне по id нужно создать свой обьект класса?
print(Friends)