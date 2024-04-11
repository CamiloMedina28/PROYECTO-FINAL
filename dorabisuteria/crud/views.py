import json
import os
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consulta, Producto, Material, Proveedor, Material, Cliente
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View


def inventario(request):
    return render (request, "login/login.html")

@login_required
def admin_dash(request):
    try: 
        if request.user.is_authenticated:
            view_producto = request.user.has_perm('crud.view_producto')
            view_proveedores = request.user.has_perm('crud.view_proveedor')
            view_material = request.user.has_perm('crud.view_material')
            view_consulta = request.user.has_perm('crud.view_consulta')
            view_empleados = request.user.has_perm('user.view_user')
            return render(request, "admin_dash/main.html", {"view_producto": view_producto, 
                                                            "view_materiales": view_material, 
                                                            "view_consulta": view_consulta, 
                                                            "view_proveedor": view_proveedores, 
                                                            "view_empleados": view_empleados})
        else: 
            messages.error(request, "Usted no ha iniciado sesión")
            return render(request, "main_dash/index.html")
    except Exception as error: 
        messages.error(request, "Ha courrido un error al procesar su solicitud" + str(error))
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

class ProductsView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        productos = list(Producto.objects.values())
        info = {"productos_en_db" : productos}
        return JsonResponse(info)

    def post(self, request):
        json_info = json.loads(request.body)
        print(json_info)
        Producto.objects.create()
        datos = {'message': 'Proceso exitoso'}

    def put(self, request):
        pass

    def delete(self, request):
        pass

class MaterialView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        materiales = list(Material.objects.values())
        proveedores = list(Proveedor.objects.values())
        datos = {"materiales_en_db": materiales, 
                "proveedores_en_db": proveedores}
        return JsonResponse(datos)

    def post(self,request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class ProveedorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        proveedores = list(Proveedor.objects.values())
        datos = {"proveedores_en_db": proveedores}
        return JsonResponse(datos)

    def post(self,request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class ConsultaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        clientes = list(Cliente.objects.values())
        consulta = list(Consulta.objects.values())
        return JsonResponse({"consultas_en_db": consulta, 
                             "clientes": clientes})

    def post(self,request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

@login_required
def products_administration(request):
    if request.user.has_perm('crud.view_producto'):
        try:
            if request.user.is_authenticated:
                permiso_adicion = request.user.has_perm('crud.add_producto')
                permiso_eliminacion = request.user.has_perm('crud.delete_producto')
                permiso_edicion = request.user.has_perm('crud.change_producto')
                productos = Producto.objects.all()
                materiales = Material.objects.all()
                return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                           "material_en_db" : materiales, 
                                                                           "permiso_adicion": permiso_adicion, 
                                                                           "permiso_eliminacion": permiso_eliminacion, 
                                                                           "permiso_edicion": permiso_edicion})
            else:
                return render(request, "/main_dash/index.html")
        except Exception as error:
            messages.error(request, "Ha ocurrido un problema al intentar procesar la solicitud" + str(error))
            return render(request, "main_dash/index.html")
    else: 
        messages.error(request, "el usuario no tiene permisos para acceder a esta sección")
        return render(request, "admin_dash/main.html")

@login_required
def prov_administration(request):
    if request.user.has_perm('crud.view_proveedor'):
        try:
            if request.user.is_authenticated:
                proveedores = Proveedor.objects.all()
                return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db": proveedores, 
                                                                             "permisos_creacion": request.user.has_perm('crud.add_proveedor'), 
                                                                             "permisos_eliminacion": request.user.has_perm('crud.delete_proveedor'), 
                                                                             "permisos_edicion": request.user.has_perm('crud.change_proveedor')})
            else:
                return render(request, "main_dash/index.html")
        except Exception as error:
            messages.error(request, "La solicitud desarrollada no puede ser resolvida.")
            return render(request, "main_dash/index.html")
    else: 
        messages.error(request, "el usuario no tiene permisos para acceder a esta sección")
        return render(request, "admin_dash/main.html")


@login_required
def insert_new_products(request):
    if request.user.has_perm('crud.add_producto'):
        try:
            if request.method == "POST":
                pro_id = request.POST.get('pro_id')
                pro_nombre = request.POST.get('pro_nombre')
                pro_precio = request.POST.get('pro_precio')
                pro_stock = request.POST.get('pro_stock')
                pro_img = request.FILES.get('pro_img')
                material_elegido = request.POST.getlist('materiales')
                folder = 'media/'
                fs = FileSystemStorage(location=folder)
                filename = fs.save(pro_img.name, pro_img)
                if pro_nombre in Producto.objects.values_list('pro_nombre', flat=True) or pro_id in Producto.objects.values_list('pro_id', flat=True):
                    messages.error(request, "El nombre o el id de producto ya existen en la base de datos")
                    productos = Producto.objects.all()
                    materiales = Material.objects.all()
                    return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                               "material_en_db" : materiales, 
                                                                                "permiso_adicion": request.user.has_perm('crud.add_producto'), 
                                                                                "permiso_eliminacion":request.user.has_perm('crud.delete_producto'), 
                                                                                "permiso_edicion": request.user.has_perm('crud.change_producto')})
                json_structure_new_product = "{"+f""""pro_id" : "{pro_id}","pro_nombre" : "{pro_nombre}", "pro_precio": "{pro_precio}", "pro_stock":"{pro_stock}", "pro_img":"{pro_img}" """ + "}" 
                json_data_new_product = json.loads(json_structure_new_product)
                nuevo_producto = Producto(pro_id = json_data_new_product['pro_id'], 
                                          pro_nombre = json_data_new_product['pro_nombre'], 
                                          pro_precio = json_data_new_product['pro_precio'], 
                                          pro_stock = json_data_new_product['pro_stock'], 
                                          pro_img = json_data_new_product['pro_img'])
                nuevo_producto.save()
                for i in material_elegido:
                    nuevo_producto.materiales.add(i)
                nuevo_producto.save()
            if request.user.is_authenticated:
                productos = Producto.objects.all()
                materiales = Material.objects.all()
                return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                           "material_en_db" : materiales, 
                                                                           "permiso_adicion": request.user.has_perm('crud.add_producto'), 
                                                                           "permiso_eliminacion":request.user.has_perm('crud.delete_producto'), 
                                                                           "permiso_edicion": request.user.has_perm('crud.change_producto')})
            else:
                return render(request, "/main_dash/index.html")
        except Exception as error:
            messages.error(request, "Ha ocurrido un error al intentar procesar su solicitud" + str(error))
            productos = Producto.objects.all()
            materiales = Material.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                       "material_en_db" : materiales,
                                                                       "permiso_adicion": request.user.has_perm('crud.add_producto'), 
                                                                        "permiso_eliminacion":request.user.has_perm('crud.delete_producto'), 
                                                                        "permiso_edicion":request.user.has_perm('crud.change_producto')})
    else: 
        messages.error(request, "Usted no tiene permiso para acceder a esta sección")
        return render(request, "admin_dash/main.html")

@login_required  
def eliminar_producto(request, pro_id_eliminar):
    if request.user.has_perm('crud.delete_producto'):
        try:
            producto = Producto.objects.get(pro_id = pro_id_eliminar)
            ruta = os.path.join(settings.BASE_DIR, 'media/' + str(producto.pro_img))
            os.remove(ruta)
            producto.delete() # DELETE FROM producto WHERE pro_id = pro_id
            productos = Producto.objects.all()
            materiales = Material.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                       "material_en_db" : materiales,
                                                                       "permiso_adicion":request.user.has_perm('crud.add_producto'),
                                                                       "permiso_eliminacion":request.user.has_perm('crud.delete_producto'),
                                                                       "permiso_edicion":request.user.has_perm('crud.change_producto')})
        except Exception as error: 
            messages.error(request, "Ha ocurrido un error al intentar procesar la solicitud: " + str(error))
            productos = Producto.objects.all()
            materiales = Material.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                       "material_en_db" : materiales,
                                                                       "permiso_adicion":request.user.has_perm('crud.add_producto'),
                                                                       "permiso_eliminacion":request.user.has_perm('crud.delete_producto'),
                                                                       "permiso_edicion":request.user.has_perm('crud.change_producto')})
    else:
        messages.error(request, "Usted no tiene los permisos suficientes para hacer esta solicitud")
        productos = Producto.objects.all()
        materiales = Material.objects.all()
        return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos, 
                                                                   "material_en_db" : materiales,
                                                                   "permiso_adicion":request.user.has_perm('crud.add_producto'),
                                                                   "permiso_eliminacion":request.user.has_perm('crud.delete_producto'),
                                                                   "permiso_eliminacion":request.user.has_perm('change.crud_producto')})


@login_required
def employees_administration(request):
    if request.user.has_perm("user.view_user"):
        if request.user.is_authenticated:
            usuario_actual = request.user
            users = User.objects.all()
            return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                       "usuario_actual": usuario_actual, 
                                                                       "permisos_edicion": usuario_actual.has_perm('user.change_user'),
                                                                       "permisos_creacion": usuario_actual.has_perm('user.add_user'), 
                                                                       "permisos_eliminacion": usuario_actual.has_perm('user.delete_user')})
        else:
            return render(request, "main_dash/index.html")
    else:
        messages.error(request, "Error, usted no tiene permisos suficientes")
        return render(request, "main_dash/index.html")

@login_required
def insert_new_prov(request):
    if request.user.has_perm('crud.add_proveedor'):
        try:
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
                return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db": proveedores,
                                                                            "permisos_creacion":request.user.has_perm('crud.add_proveedor'),
                                                                            "permisos_eliminacion":request.user.has_perm('crud.delete_proveedor'),
                                                                            "permisos_edicion":request.user.has_perm('crud.change_proveedor')})
            else:
                return render(request, "main_dash/index.html")
        except Exception as error:
            messages.error(request, "Su solicitud no puedo ser procesada: " + str(error))
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"proveedores_en_db" : proveedores,
                                                                        "permisos_creacion":request.user.has_perm('crud.add_proveedor'),
                                                                        "permisos_eliminacion":request.user.has_perm('crud.delete_proveedor'),
                                                                        "permisos_edicion":request.user.has_perm('crud.change_proveedor')})
    else:
        messages.error(request, "Usted no tiene los permisos sufiecientes para desarrollar esta acción")
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/productos_admin.html", {"proveedores_en_db" : proveedores,
                                                                    "permisos_creacion":request.user.has_perm('crud.add_proveedor'),
                                                                    "permisos_eliminacion":request.user.has_perm('crud.delete_proveedor'),
                                                                    "permisos_edicion":request.user.has_perm('crud.change_proveedor')})

@login_required
def eliminar_proveedores(request, prov_nit_eliminar):
    if request.user.has_perm('crud.delete_proveedor'):
        try:
            proveedor = Proveedor.objects.get(prov_nit = prov_nit_eliminar)
            proveedor.delete() # DELETE FROM proveedor WHERE prov_nit = prov_nit_eliminar
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db" : proveedores, 
                                                                         "permisos_eliminacion": request.user.has_perm('crud.delete_proveedor'), 
                                                                         "permisos_creacion": request.user.has_perm('crud.add_proveedor'),
                                                                         "permisos_edicion": request.user.has_perm('crud.change_proveedor')})
        except Exception as error:
            messages.error(request, "Ha ocurrido un error inesperado: " + str(error))
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db" : proveedores,
                                                                        "permisos_eliminacion":request.user.has_perm('crud.delete_proveedor'),
                                                                        "permisos_creacion": request.user.has_perm('crud.add_proveedor'),
                                                                        "permisos_edicion": request.user.has_perm('crud.change_proveedor')})
    else:
        messages.error(request, "Usted no tiene permisos para desarrollar esta acción")
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db" : proveedores,
                                                                    "permisos_eliminacion":request.user.has_perm('crud.delete_proveedor'),
                                                                    "permisos_creacion": request.user.has_perm('crud.add_proveedor'),
                                                                    "permisos_edicion": request.user.has_perm('crud.change_proveedor')})

@login_required
def materiales_admin(request):
    if request.user.has_perm('crud.view_material'):
        if request.user.is_authenticated:
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                        "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
        else:
            return render(request, "admin_dash/index.html")
    else:
        messages.error(request, "Usted no tiene los permisos suficientes para desarrollar esta acción")
        return render(request, "main_dash/main.html")    

@login_required
def eliminar_materiales(request, mat_id_eliminar):
    if request.user.has_perm('crud.delete_material'):
        try:
            proveedor = Material.objects.get(mat_id = mat_id_eliminar)
            proveedor.delete() # DELETE FROM material WHERE mat_id = mat_id_eliminar
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db" : materiales,
                                                                         "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
        except Exception as error:
            messages.error(request, "Ha ocurrido un error fatal: " + str(error))
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db" : materiales, 
                                                                        "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
    else: 
        messages.error(request, "Usted no tiene los permisos para desarrollar esta acción")
        materiales = Material.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db" : materiales, 
                                                                    "proveedores_en_db": proveedores, 
                                                                    "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                    "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                    "permisos_eliminacion": request.user.has_perm('crud.delete_material')})

@login_required
def insert_new_mat(request):
    if request.user.has_perm('crud.insert_material'):
        try:
            if request.method == "POST":
                mat_id = request.POST.get('mat_id')
                mat_pro_id = request.POST.get('mat_prov_id')
                stock = request.POST.get('stock')
                nombre = request.POST.get('nombre')
                if mat_id in Material.objects.values_list('mat_id', flat=True) or nombre in Material.objects.values_list('nombre', flat=True):
                    messages.error(request, "El nombre o el id de producto ya existen en la base de datos")
                    materiales = Material.objects.all()
                    proveedores = Proveedor.objects.all()
                    return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales,
                                                                                "proveedores_en_db" : proveedores, 
                                                                                "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                                "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                                "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
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
                return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                            "proveedores_en_db": proveedores, 
                                                                            "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                            "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                            "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
        except Exception as error:
            messages.error(request, "Ha ocurrido un grave error: " + str(error))
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                        "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
    else:
        messages.error(request, "Usted no tiene permisos para desarrollar esta acción")
        materiales = Material.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                    "proveedores_en_db": proveedores, 
                                                                    "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                    "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                    "permisos_eliminacion": request.user.has_perm('crud.delete_material')})

@login_required
def clientes_admin(request):
    if request.user.has_perm('crud.view_consulta'):
        consulta = Consulta.objects.all()
        return render(request, "admin_dash/clientes_admin.html", {"consultas_en_db": consulta, 
                                                                  "permisos_eliminacion": request.user.has_perm('crud.delete_consulta')})
    else:
        messages.error(request, "Usted no tiene permiso para acceder a esta sección")
        return render(request, "admin_dash/main.html")

@login_required
def eliminar_consulta(request, id_consulta_eliminar):
    if request.user.has_perm('crud.delete_consulta'):
        consulta_eliminar = Consulta.objects.get(id = id_consulta_eliminar)
        consulta_eliminar.delete()
        consulta = Consulta.objects.all()
        return render(request, "admin_dash/clientes_admin.html", {"consultas_en_db": consulta,
                                                                  "permisos_eliminacion": request.user.has_perm('crud.delete_consulta')})
    else:
        messages.error(request, "Usted no tiene permiso para acceder a esta sección")
        consulta = Consulta.objects.all()
        return render(request, "admin_dash/clientes_admin.html", {"consultas_en_db": consulta,
                                                                  "permisos_eliminacion": request.user.has_perm('crud.delete_consulta')})

@login_required
def create_new_user(request):
    if request.user.has_perm('user.add_user'):
        try:
            if request.method == "POST":
                usuario_actual = request.user
                new_user_first_name = request.POST.get('new_user_first_name')
                new_user_last_name = request.POST.get('new_user_last_name')
                new_username = request.POST.get('new_username')
                new_user_email = request.POST.get('new_user_email')
                new_user_password = request.POST.get('new_user_password')
                if new_user_email in User.objects.values_list('email', flat=True) or new_username in User.objects.values_list('username', flat=True):
                    messages.error(request, "El nombre de usuario o el email ya existen en la base de datos")
                    users = User.objects.all()
                    return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users,
                                                                                "usuario_actual": usuario_actual,
                                                                               "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                               "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                               "permisos_edicion":request.user.has_perm('user.change_user')})
                json_structure_new_user = "{"+f""""first_name" : "{new_user_first_name}", "last_name": "{new_user_last_name}", "usuario":"{new_username}", "password" : "{new_user_password}", "email":"{new_user_email}" """ + "}" 
                json_data_new_user = json.loads(json_structure_new_user)
                nuevo_usuario = User.objects.create_user(json_data_new_user['usuario'],
                                                         json_data_new_user['email'],
                                                         json_data_new_user['password'])
                nuevo_usuario.first_name = json_data_new_user['first_name']
                nuevo_usuario.last_name = json_data_new_user['last_name']
                nuevo_usuario.is_staff = 1
                nuevo_usuario.save()
                users = User.objects.all()
                return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                           "usuario_actual":usuario_actual,
                                                                            "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                            "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                            "permisos_edicion":request.user.has_perm('user.change_user')})
            else:
                messages.error("No se pudo crear el nuevo usuario: " + "error de administrador")
                users = User.objects.all()
                usuario_actual = request.user
                return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                           "usuario_actual": usuario_actual,
                                                                            "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                            "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                            "permisos_edicion":request.user.has_perm('user.change_user')})
        except Exception as error:
            messages.error(request, "Ha ocurrido un grave error: " + str(error))
            users = User.objects.all()
            return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                        "usuario_actual": usuario_actual,
                                                                        "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                        "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                        "permisos_edicion":request.user.has_perm('user.change_user')})
    else:
        messages.error(request, "Usted no tiene los permisos suficientes para desarrollar esta acción")
        users = User.objects.all()
        return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                    "usuario_actual": usuario_actual,
                                                                    "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                    "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                    "permisos_edicion":request.user.has_perm('user.change_user')})    
    
@login_required
def eliminar_usuarios(request, id_usuario_eliminar):
    if request.user.has_perm('user.delete_user'):
        usuario_eliminar = User.objects.get(id = id_usuario_eliminar)
        usuario_eliminar.delete()
        users = User.objects.all()
        usuario_actual = request.user
        return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                    "usuario_actual" : usuario_actual, 
                                                                    "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                    "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                    "permisos_edicion":request.user.has_perm('user.change_user')})
    else: 
        messages.error(request, "Usted no tiene los permisos suifiecientes para desarrollar esta acción")
        users = User.objects.all()
        usuario_actual = request.user
        return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users, 
                                                                    "usuario_actual" : usuario_actual, 
                                                                    "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                    "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                    "permisos_edicion":request.user.has_perm('user.change_user')})

@login_required
def proveedores_update(request, prov_nit_edit):
    if request.user.has_perm('user.change_proveedor'):
        proveedor = Proveedor.objects.get(prov_nit = prov_nit_edit)
        return render(request, "update_templates/proveedores_update.html", {"proveedor_editar": proveedor})
    else:
        proveedor = Proveedor.objects.get(prov_nit = prov_nit_edit)
        return render(request, "update_templates/proveedores_update.html", {"proveedor_editar": proveedor})

@login_required
def editar_proveedor(request):
    if request.user.has_perm('user.change_proveedor'):
        try:
            if request.method == "POST":
                prov_nit = request.POST.get('prov_nit')
                prov_razon_social = request.POST.get('prov_razon_social')
                prov_telefono = request.POST.get('prov_telefono')
                proveedor = Proveedor.objects.get(prov_nit = prov_nit)
                json_structure_new_proveedor = "{"+f""""prov_nit" : "{prov_nit}","prov_razon_social" : "{prov_razon_social}", "prov_telefono": "{prov_telefono}" """ + "}" 
                json_data_new_proveedor = json.loads(json_structure_new_proveedor)
                proveedor.prov_nit = json_data_new_proveedor['prov_nit']
                proveedor.prov_razon_social = json_data_new_proveedor['prov_razon_social']
                proveedor.prov_telefono = json_data_new_proveedor['prov_telefono']
                proveedor.save()
            if request.user.is_authenticated:
                proveedores = Proveedor.objects.all()
                return render(request, "admin_dash/proveedores_admin.html", {"proveedores_en_db": proveedores, 
                                                                             "permisos_creacion":request.user.has_perm('crud.add_proveedor'), 
                                                                             "permisos_eliminacion": request.user.has_perm('crud.delete_proveedor'), 
                                                                             "permisos_edicion": request.user.has_perm('crud.change_proveedor')})
            else:
                return render(request, "main_dash/index.html")
        except Exception as error:
            messages.error(request, "Su solicitud no puedo ser procesada: " + str(error))
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/productos_admin.html", {"proveedores_en_db" : proveedores, 
                                                                             "permisos_creacion":request.user.has_perm('crud.add_proveedor'), 
                                                                             "permisos_eliminacion": request.user.has_perm('crud.delete_proveedor'), 
                                                                             "permisos_edicion": request.user.has_perm('crud.change_proveedor')})
    else:
        messages.error(request, "Usted no tiene los permisos necesarios para desarrollar esta acción.")
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/productos_admin.html", {"proveedores_en_db" : proveedores, 
                                                                             "permisos_creacion":request.user.has_perm('crud.add_proveedor'), 
                                                                             "permisos_eliminacion": request.user.has_perm('crud.delete_proveedor'), 
                                                                             "permisos_edicion": request.user.has_perm('crud.change_proveedor')})    

@login_required
def materiales_update(request, material_id):
    if request.user.has_perm('crud.change_material'):
        material = Material.objects.get(mat_id = material_id)
        proveedores = Proveedor.objects.all()
        return render(request, "update_templates/materiales_update.html", {"materiales" : material, "proveedores_en_db": proveedores})
    else:
        if request.user.has_perm('crud.view_material'):
            messages.error(request, "Usted no tiene los permisos suficientes para desarrollar esta acción.")
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                        "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
        else: 
            return render(request, "admin_dash/main.html")


@login_required
def update_material(request):
    if request.user.has_perm('crud.change_material'):
        try:
            if request.method == "POST":
                mat_id_given = request.POST.get('mat_id')
                mat_pro_id = request.POST.get('mat_prov_id')
                stock = request.POST.get('stock')
                nombre = request.POST.get('nombre')
                material = Material.objects.get(mat_id = mat_id_given)
                json_structure_new_material = "{"+f""""mat_id" : "{mat_id_given}", "stock": "{stock}", "nombre":"{nombre}" """ + "}" 
                json_data_new_material = json.loads(json_structure_new_material)
                proveedor = Proveedor.objects.get(prov_nit = mat_pro_id)
                material.mat_id = json_data_new_material['mat_id']
                material.mat_prov_id = proveedor
                material.stock = json_data_new_material['stock']
                material.nombre = json_data_new_material['nombre']
                material.save()
                materiales = Material.objects.all()
                proveedores = Proveedor.objects.all()
                return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                            "proveedores_en_db": proveedores, 
                                                                            "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                            "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                            "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
        except Exception as error:
            messages.error(request, "Ha ocurrido un grave error: " + str(error))
            materiales = Material.objects.all()
            proveedores = Proveedor.objects.all()
            return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                        "proveedores_en_db": proveedores, 
                                                                        "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                        "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                        "permisos_eliminacion": request.user.has_perm('crud.delete_material')})
    else:
        messages.error(request, "Usted no tiene los permisos suficientes para desarrollar esta acción.")
        materiales = Material.objects.all()
        proveedores = Proveedor.objects.all()
        return render(request, "admin_dash/materiales_admin.html", {"materiales_en_db": materiales, 
                                                                    "proveedores_en_db": proveedores, 
                                                                    "permisos_creacion": request.user.has_perm('crud.add_material'), 
                                                                    "permisos_edicion": request.user.has_perm('crud.change_material'), 
                                                                    "permisos_eliminacion": request.user.has_perm('crud.delete_material')})

@login_required
def update_productos(request, id_actualizacion):
    if request.user.has_perm('user.change_proveedor'):
        producto = Producto.objects.get(pro_id = id_actualizacion)
        materiales_total = Material.objects.all()
        materiales_producto = producto.materiales.all()
        mat_send_prod = []
        mat_send_no_prod = []
        for i in materiales_total:
            mat_send_prod.append(i) if i in materiales_producto else mat_send_no_prod.append(i)
        return render(request, "update_templates/productos_update.html", {"producto_editar": producto,
                                                                          "material_en_db": mat_send_no_prod, 
                                                                          "materiales_producto": mat_send_prod})
    else:
        productos = Producto.objects.all()
        materiales = Material.objects.all()
        return render(request, "admin_dash/productos_admin.html", {"productos_en_db" : productos,
                                                                   "material_en_db" : materiales,
                                                                       "permiso_adicion":request.user.has_perm('crud.add_producto'),
                                                                       "permiso_eliminacion":request.user.has_perm('crud.delete_producto'),
                                                                       "permiso_eliminacion":request.user.has_perm('change.crud_producto')})
    
@login_required
def actualizar_producto(request):
    pass

@login_required
def empleados_update(request, id_empleado):
    if request.user.has_perm('user.view_user'):
        lista_permisos = ['crud.add_producto', 
                          'crud.view_producto', 
                          'crud.change_producto', 
                          'crud.delete_producto',
                          'crud.add_material', 
                          'crud.view_material', 
                          'crud.change_material', 
                          'crud.delete_material',
                          'crud.add_proveedor', 
                          'crud.view_proveedor', 
                          'crud.change_proveedor', 
                          'crud.delete_proveedor',
                          'crud.delete_consulta', 
                          'crud.view_consulta'] 
        users = User.objects.get(id = id_empleado)
        permisos_usuario = users.get_all_permissions()
        return render(request, 'update_templates/empleados_update.html', {"usuario":users,
                                                                     "permisos":lista_permisos, 
                                                                     "permisos_usuario":permisos_usuario})
    else: pass

@login_required
def actualizar_empleado(request, id_user):
    if request.user.has_perm('crud.change_material'):
        lista_permisos = ['crud.add_producto', 
                          'crud.view_producto', 
                          'crud.change_producto', 
                          'crud.delete_producto',
                          'crud.add_material', 
                          'crud.view_material', 
                          'crud.change_material', 
                          'crud.delete_material',
                          'crud.add_proveedor', 
                          'crud.view_proveedor', 
                          'crud.change_proveedor', 
                          'crud.delete_proveedor',
                          'crud.delete_consulta', 
                          'crud.view_consulta'] 
        id_permiso = [49, 52, 50, 51, 45, 48, 46, 47, 41, 44, 42 ,43 ,39, 40]
        if request.method == 'POST':
            permisos_validados = [request.POST.get(i,None) for i in lista_permisos if request.POST.get(i,None) is not None]
            apellido = request.POST.get('new_user_last_name')
            email = request.POST.get('new_user_email')
            usuario_editar = User.objects.get(id = id_user)
            permisos_usuario = usuario_editar.get_all_permissions()
            usuario_editar.last_name = apellido
            usuario_editar.email = email
            for i in permisos_validados:
                index = lista_permisos.index(i)
                if i not in permisos_usuario:
                    usuario_editar.user_permissions.add(id_permiso[index])
            for i in permisos_usuario:
                index = lista_permisos.index(i)
                if i not in permisos_validados:
                    usuario_editar.user_permissions.remove(id_permiso[index])

        users = User.objects.all()
        usuario_actual = request.user
        return render(request, "admin_dash/empleados_admin.html", {"usuarios_en_db" : users,
                                                                    "usuario_actual": usuario_actual,
                                                                   "permisos_eliminacion":request.user.has_perm('user.delete_user'), 
                                                                   "permisos_creacion":request.user.has_perm('user.add_user'),
                                                                   "permisos_edicion":request.user.has_perm('user.change_user')})
    