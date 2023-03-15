from django.urls import include, path
from authentication import api
from rest_framework.routers import DefaultRouter

app_name = 'authentication'

urlpatterns = [
    path('login/', api.LoginAPI.as_view(), name='login'),
    path('register/', api.RegisterAPI.as_view(), name='register'),
]
