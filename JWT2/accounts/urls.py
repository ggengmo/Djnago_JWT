# accounts > urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('join/', include('dj_rest_auth.registration.urls')),
    path('mypage/', views.mypage, name='mypage'),
]
