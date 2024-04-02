from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('inventario', views.inventario, name="inventario"),
    path('user_login', views.user_login, name="user_login"), 
    path('client_return', views.client_return, name="client_return"), 
    path('admin_dash', views.admin_dash, name="admin_dash"),
    path('products_administration', views.products_administration, name="products_administration"), 
    path('prov_administration', views.prov_administration, name="prov_administration"), 
    path('employees_administration', views.employees_administration, name="employees_administration"), 
    path('user_logout', views.user_logout, name="user_logout"), 
    path('insert_new_products', views.insert_new_products, name="insert_new_products")
]