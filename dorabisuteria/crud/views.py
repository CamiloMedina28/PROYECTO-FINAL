import json
import os
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Material, Proveedor, Material
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.

def inventario(request):
    return render (request, "login/login.html")

@login_required
def admin_dash(request):
    if request.user.is_authenticated:
        return render(request, "admin_dash/main.html")
    else: 
        messages.error(request, "Usted no ha iniciado sesión")
        return render(request, "main_dash/index.html")

def user_login(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        contrasenia = request.POST.get('contrasenia')
    authentication = authenticate(request, username = usuario, password = contrasenia)
    if authentication:
        login(request, authentication)
        return redirect(admin_dash)
    else:
        messages.error(request, "Inicio de sesión incorrecto, por favor verifique y vuelva a intentarlo.")
        return render (request, "login/login.html")

def client_return(request):
    return render(request, "main_dash/index.html")

def user_logout(request):
    logout(request)
    return render(request, "main_dash/index.html")

@login_required
def products_administration(request):
    if request.user.is_authenticated:
        productos = Producto.objects.all()
        materiales = Material.objects.all()
        print(materiales)
        return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, "material_en_db" : materiales})
    else:
        return render(request, "/main_dash/index.html")

@login_required
def prov_administration(request):
    if request.user.is_authenticated:
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db": proveedores})
    else:
        return render(request, "main_dash/index.html")

@login_required
def insert_new_products(request):
    if request.method == "POST":
        pro_id = request.POST.get('pro_id')
        pro_nombre = request.POST.get('pro_nombre')
        pro_precio = request.POST.get('pro_precio')
        pro_stock = request.POST.get('pro_stock')
        pro_img = request.FILES.get('pro_img')
        materiales = request.POST.get('materiales')
        folder = 'media/'
        fs = FileSystemStorage(location=folder)
        filename = fs.save(pro_img.name, pro_img)
        if pro_nombre in Producto.objects.values_list('pro_nombre', flat=True) or pro_id in Producto.objects.values_list('pro_id', flat=True):
            messages.error(request, "El nombre o el id de producto ya existen en la base de datos")
            productos = Producto.objects.all()
            materiales = Material.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, "material_en_db" : materiales})
        json_structure_new_product = "{"+f""""pro_id" : "{pro_id}","pro_nombre" : "{pro_nombre}", "pro_precio": "{pro_precio}", "pro_stock":"{pro_stock}", "pro_img":"{pro_img}" """ + "}" 
        json_data_new_product = json.loads(json_structure_new_product)
        nuevo_producto = Producto(pro_id = json_data_new_product['pro_id'], 
                                  pro_nombre = json_data_new_product['pro_nombre'], 
                                  pro_precio = json_data_new_product['pro_precio'], 
                                  pro_stock = json_data_new_product['pro_stock'], 
                                  pro_img = json_data_new_product['pro_img'])
        nuevo_producto.save()
    if request.user.is_authenticated:
        productos = Producto.objects.all()
        materiales = Material.objects.all()
        return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, "material_en_db" : materiales})
    else:
        return render(request, "/main_dash/index.html")
    
def eliminar_producto(request, pro_id_eliminar):
    producto = Producto.objects.get(pro_id = pro_id_eliminar)
    ruta = os.path.join(settings.BASE_DIR, 'media/' + str(producto.pro_img))
    os.remove(ruta)
    producto.delete() # DELETE FROM producto WHERE pro_id = pro_id
    productos = Producto.objects.all()
    materiales = Material.objects.all()
    return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, "material_en_db" : materiales})


def employees_administration(request):
    if request.user.is_authenticated:
        return render(request, "admin_dash/empleados_admin.html")
    else:
        return render(request, "main_dash/index.html")
    
@login_required
def insert_new_prov(request):
    if request.method == "POST":
        prov_nit = request.POST.get('prov_nit')
        prov_razon_social = request.POST.get('prov_razon_social')
        prov_telefono = request.POST.get('prov_telefono')
        if prov_nit in Proveedor.objects.values_list('prov_nit', flat=True) or prov_razon_social in Proveedor.objects.values_list('prov_razon_social', flat=True):
            messages.error(request, "El nombre o el id de producto ya existen en la base de datos")
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"proveedores_en_db" : proveedores})
        json_structure_new_proveedor = "{"+f""""prov_nit" : "{prov_nit}","prov_razon_social" : "{prov_razon_social}", "prov_telefono": "{prov_telefono}" """ + "}" 
        json_data_new_proveedor = json.loads(json_structure_new_proveedor)
        nuevo_proveedor = Proveedor(prov_nit = json_data_new_proveedor['prov_nit'], 
                                  prov_razon_social = json_data_new_proveedor['prov_razon_social'], 
                                  prov_telefono = json_data_new_proveedor['prov_telefono'])
        nuevo_proveedor.save()
    if request.user.is_authenticated:
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db": proveedores})
    else:
        return render(request, "main_dash/index.html")

@login_required
def eliminar_proveedores(request, prov_nit_eliminar):
    proveedor = Proveedor.objects.get(prov_nit = prov_nit_eliminar)
    proveedor.delete() # DELETE FROM proveedor WHERE prov_nit = prov_nit_eliminar
    proveedores = Proveedor.objects.all()
    return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db" : proveedores})

@login_required
def materiales_admin(request):
    if request.user.is_authenticated:
        materiales = Material.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, "proveedores_en_db": proveedores})
    else:
        return render(request, "main_dash/index.html")
    pass

def eliminar_materiales(request, mat_id_eliminar):
    proveedor = Material.objects.get(mat_id = mat_id_eliminar)
    proveedor.delete() # DELETE FROM material WHERE mat_id = mat_id_eliminar
    materiales = Material.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db" : materiales, "proveedores_en_db": proveedores})

def insert_new_mat(request):
    if request.method == "POST":
        mat_id = request.POST.get('mat_id')
        mat_pro_id = request.POST.get('mat_prov_id')
        stock = request.POST.get('stock')
        nombre = request.POST.get('nombre')
        if mat_id in Material.objects.values_list('mat_id', flat=True) or nombre in Material.objects.values_list('nombre', flat=True):
            messages.error(request, "El nombre o el id de producto ya existen en la base de datos")
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"materiales_en_db": materiales,"proveedores_en_db" : proveedores})
        json_structure_new_material = "{"+f""""mat_id" : "{mat_id}", "stock": "{stock}", "nombre":"{nombre}" """ + "}" 
        json_data_new_material = json.loads(json_structure_new_material)
        proveedor = Proveedor.objects.get(prov_nit = mat_pro_id)
        nuevo_material = Material(mat_id = json_data_new_material['mat_id'], 
                                  mat_prov_id = proveedor, 
                                  stock = json_data_new_material['stock'], 
                                  nombre = json_data_new_material['nombre'])
        nuevo_material.save()
        materiales = Material.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, "proveedores_en_db": proveedores})