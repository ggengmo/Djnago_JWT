# JWT2 > testrequest.py

import requests

HOST = 'http://localhost:8000'
LOGIN_URL = HOST + '/accounts/login/'
MYPAGE_URL = HOST + '/accounts/mypage/'

LOGIN_INFO = {
    "email": "rudah365dlf@gmail.com",
    "password": "qwer1234@"
}

response = requests.post(LOGIN_URL, data=LOGIN_INFO)
print(response.status_code)
print(response.text)
print(response.json()['access_token'])

token = response.json()['access_token']

header = {
    'Authorization': 'Bearer ' + token
}

response = requests.get(MYPAGE_URL, headers=header)
print(response.json())
