from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('send_info', views.send_info, name="send_info")
]