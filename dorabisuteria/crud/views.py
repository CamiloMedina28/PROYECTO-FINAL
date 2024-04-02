import json
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Material
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
        return render(request, "admin_dash/proveedores_admin.html")
    else:
        return render(request, "main_dash/index.html")

@login_required
def insert_new_products(request):
    if request.method == "POST":
        pro_id = request.POST.get('pro_id')
        pro_nombre = request.POST.get('pro_nombre')
        pro_precio = request.POST.get('pro_precio')
        pro_stock = request.POST.get('pro_stock')
        pro_img = request.POST.get('pro_img')
        materiales = request.POST.get('materiales')
        print(materiales)
        if pro_nombre in Producto.objects.values_list('pro_nombre', flat=True) or pro_id in Producto.objects.values_list('pro_id', flat=True):
            messages.error("El nombre o el id de producto ya existen en la base de datos")
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
    # try:
    #     if request.method == "POST":
    #         name = request.POST.get('nombre')
    #         apellido = request.POST.get('apellido')
    #         correo = request.POST.get('correo')
    #         duda = request.POST.get('duda')
    #     json_structure_new_client =  "{"+f""""Nombre" : "{name}","Apellido" : "{apellido}", "correo": "{correo}", "duda":"{duda}" """ + "}" 
    #     json_data_new_client = json.loads(json_structure_new_client)
    #     nuevo_cliente = Cliente(per_primer_nombre = json_data_new_client['Nombre'],
    #                            per_primer_apellido = json_data_new_client['Apellido'], 
    #                            per_email = json_data_new_client['correo'])
    #     nuevo_cliente.save()
    #     nueva_duda = Consulta(con_cli_per_id = nuevo_cliente,
    #                           con_comentario = json_data_new_client['duda'])
    #     nueva_duda.save()
    # except Exception as error: 
    #     messages.error(request, "La información no pudo ser enviada" + str(error))
    # else:
    #     messages.success(request, "El dato ha sido ingresado con éxito")
    # finally:
    #     return render(request, "main_dash/index.html")
    pass

def employees_administration(request):
    if request.user.is_authenticated:
        return render(request, "admin_dash/empleados_admin.html")
    else:
        return render(request, "main_dash/index.html")