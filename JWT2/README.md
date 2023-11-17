# 1. 프로젝트 설정
## 폴더 생성 및 이동
mkdir jWT_test

cd JWT_test

## 가상환경 및 Django 설치
python -m venv venv

pip install django

## 프로젝트 및 앱 생성
django-admin startproject JWT_TEST .

python manage.py startapp accounts

## JTW2 > JWT_TEST > settings.py
INSTALLED_APPS = [
    '''
    생략
    '''
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'accounts',
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

## 유저 관리 기능 추가
## accounts > managers.py
# accounts > managers.py

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('이메일은 필수입니다!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("슈퍼유저는 'is_staff'가 반드시 True여야 합니다!"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("슈퍼유저는 'is_superuser'가 반드시 True여야 합니다!"))
        return self.create_user(email, password, **extra_fields)


## 모델 생성
## accounts > models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

GENDER_CHOICES = (
    ('male', '남자'),
    ('female', '여자'),
)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('이메일'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.email

## 모델 선언
## JWT2 > JWT_TEST > settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'

## DB 적용
python manage.py makemigrations
python manage.py migrate

## admin 페이지에서 모델을 관리하기위해 등록
## accounts > admin.py

from django.contrib import admin
from accounts.models import CustomUser

admin.site.register(CustomUser)

# 2. 회원가입 구현
## 라이브러리 설치
pip install -r requirements.txt

## 설치한 라이브러리 추가
## JWT2 > JWT_TEST > settings.py
INSTALLED_APPS = [
    # 설치한 라이브러리
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    '''
    생략
    '''
]

## JWT2 > JWT_TEST > settings.py 상단에 추가
from datetime import timedelta

## JWT2 > JWT_TEST > settings.py 하단에 추가
## dj-rest-auth
REST_USE_JWT = True # JWT 사용 여부
JWT_AUTH_COOKIE = 'my-app-auth' # 호출할 Cookie Key 값
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' # Refresh Token Cookie Key 값

## django-allauth
SITE_ID = 1 # 해당 도메인 id
ACCOUNT_UNIQUE_EMAIL = True # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # 사용자 이름 필드 지정
ACCOUNT_USERNAME_REQUIRED = False # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = 'none' # email 인증 필수 여부

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # AccessToken 유효 기간 설정
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # RefreshToken 유효 기간 설정
}

## JWT2 > JWT_TEST > settings.py의 INSTALLED_APPS 하단에 추가
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

## 마이그레이션
python manage.py migrate

# JWT2 > JWT_TEST > urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

## accounts > urls.py
from django.urls import path, include

urlpatterns = [
    path('join/', include('dj_rest_auth.registration.urls')),
]

# 3. 로그인 구현
# accounts > urls.py

from django.urls import path, include

urlpatterns = [
    path('', include('dj_rest_auth_urls')),
    path('join/', include('dj_rest_auth.registration.urls')),
]

## 'pkg_resources' 오류 발생시
## ImportError: Could not import 'rest_framework_simplejwt.authentication.JWTAuthentication' for API setting 'DEFAULT_AUTHENTICATION_CLASSES'. ModuleNotFoundError: No module named 'pkg_resources'.
pip install --upgrade setuptools

# 4. 테스트
## 회원가입, 로그인, 토큰 여부 확인
## 회원가입
{
    "email": "rudah365dlf@gmail.com",
    "password1": "qwer1234@",
    "password2": "qwer1234@"
}

## 로그인
{
    "email": "rudah365dlf@gmail.com",
    "password": "qwer1234@"
}

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAwNTk5LCJpYXQiOjE3MDAxOTY5OTksImp0aSI6Ijg4ZmE3MGZhNDA4YTQxZmI5YmRkODAxYWQyYTc2MjlhIiwidXNlcl9pZCI6MX0.xzwhGFG8oiUPqfYCFQYZV9Wvjgz0akfngYS2vGACg-Q",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4MzM5OSwiaWF0IjoxNzAwMTk2OTk5LCJqdGkiOiIyM2RkYjNlOWE4YTk0OGQ0OTYzOTYyNTExNjJhY2VlYiIsInVzZXJfaWQiOjF9.5r3xBZO0zJKMv4DVDd_S4nlvYdj54xrt73Sx_CrMOfk",
    "user": {
        "pk": 1,
        "email": "rudah365dlf@gmail.com",
        "first_name": "",
        "last_name": ""
    }
}

## 토큰 여부 확인
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAwNTk5LCJpYXQiOjE3MDAxOTY5OTksImp0aSI6Ijg4ZmE3MGZhNDA4YTQxZmI5YmRkODAxYWQyYTc2MjlhIiwidXNlcl9pZCI6MX0.xzwhGFG8oiUPqfYCFQYZV9Wvjgz0akfngYS2vGACg-Q

# 5. 마이페이지 생성
## accounts > urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('join/', include('dj_rest_auth.registration.urls')),
    path('mypage/', views.mypage, name='mypage'),
]

## accounts > views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    content = {'message': f"반갑습니다, {request.user.email}님!"}
    return Response(content)

# 6. 마이페이지 테스트
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


## console
200
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAzNTk5LCJpYXQiOjE3MDAxOTk5OTksImp0aSI6IjE0YTA1YmVkNGUwZTRjMmNiMzgxNThjYzdhMTlmMTIyIiwidXNlcl9pZCI6MX0.4ancdd6qL1QZcTMqB0EpZ1zQwUaWo9DcTF_lmm-snwg","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI4NjM5OSwiaWF0IjoxNzAwMTk5OTk5LCJqdGkiOiJhZWExYzRlYWFkMzA0NmViODBlMGRiZTdhZTJkOWIzMyIsInVzZXJfaWQiOjF9.fR4D-qcZn6hJP2OH56uYIZEy1Howk8Qt323NyiUL300","user":{"pk":1,"email":"rudah365dlf@gmail.com","first_name":"","last_name":""}}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjAzNTk5LCJpYXQiOjE3MDAxOTk5OTksImp0aSI6IjE0YTA1YmVkNGUwZTRjMmNiMzgxNThjYzdhMTlmMTIyIiwidXNlcl9pZCI6MX0.4ancdd6qL1QZcTMqB0EpZ1zQwUaWo9DcTF_lmm-snwg
{'message': '반갑습니다, rudah365dlf@gmail.com님!'}
