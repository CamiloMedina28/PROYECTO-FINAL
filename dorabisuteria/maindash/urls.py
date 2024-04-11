from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('send_info', views.send_info, name="send_info"),
    path('index', views.index, name="index"), 
    path('nosotros', views.nosotros, name="nosotros"), 
    path('productos', views.productos, name='productos'), 
    path('contactanos/<id_contacto>', views.contactanos, name="contactanos"), 
    path('send_info_req', views.send_info_req, name="send_info_req")
]