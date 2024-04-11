from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *

urlpatterns = [
    path('gestion_productos/', ProductsView.as_view(), name="gestion_productos"),
    path('gestion_materiales/', MaterialView.as_view(), name="gestion_materiales"),
    path('gestion_proveedores/', ProveedorView.as_view(), name="gestion_proveedores"),
    path('gestion_consultas/', ConsultaView.as_view(), name="gestion_consultas/"),
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
    path('eliminar_materiales/<mat_id_eliminar>', views.eliminar_materiales, name="eliminar_materiales"),
    path('insert_new_prov', views.insert_new_prov, name="insert_new_prov"), 
    path('eliminar_proveedores/<prov_nit_eliminar>', views.eliminar_proveedores, name="eliminar_proveedores"), 
    path('materiales_admin', views.materiales_admin, name="materiales_admin"), 
    path('insert_new_mat', views.insert_new_mat, name="insert_new_mat"), 
    path('clientes_admin', views.clientes_admin, name="clientes_admin"), 
    path('eliminar_consulta/<id_consulta_eliminar>', views.eliminar_consulta, name="eliminar_consulta"), 
    path('create_new_user', views.create_new_user, name="create_new_user"), 
    path('eliminar_usuarios/<id_usuario_eliminar>', views.eliminar_usuarios, name="eliminar_usuarios"), 
    path('proveedores_update/<prov_nit_edit>', views.proveedores_update, name="proveedores_update"), 
    path('editar_proveedor', views.editar_proveedor, name="editar_proveedor"), 
    path('materiales_update/<material_id>', views.materiales_update, name="materiales_update"), 
    path('update_material', views.update_material, name="update_material"), 
    path('update_productos/<id_actualizacion>', views.update_productos, name="update_productos"), 
    path('actualizar_producto', views.actualizar_producto, name="actualizar_producto"), 
    path('empleados_update/<id_empleado>', views.empleados_update, name="empleados_update"), 
    path('actualizar_empleado/<id_user>', views.actualizar_empleado, name="actualizar_empleado")
] 
