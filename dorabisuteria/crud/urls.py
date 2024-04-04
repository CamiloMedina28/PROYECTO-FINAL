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
    path('insert_new_products', views.insert_new_products, name="insert_new_products"), 
    path('eliminar_producto/<pro_id_eliminar>', views.eliminar_producto, name="eliminar_producto"), 
    path('insert_new_prov', views.insert_new_prov, name="insert_new_prov"), 
    path('eliminar_proveedores/<prov_nit_eliminar>', views.eliminar_proveedores, name="eliminar_proveedores"), 
    path('materiales_admin', views.materiales_admin, name="materiales_admin"), 
    path('insert_new_mat', views.insert_new_mat, name="insert_new_mat")
]

