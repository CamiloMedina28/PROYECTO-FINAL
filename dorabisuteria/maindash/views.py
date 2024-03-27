import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .models import Cliente
from .models import Consulta

# Create your views here.

def index(request):
    return render (request, "main_dash/index.html")

def nosotros(request):
    return render(request, "main_dash/nosotros.html")

def productos(request):
    return render(request, "main_dash/productos.html")

def send_info(request):
    try:
        if request.method == "POST":
            name = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            duda = request.POST.get('duda')
        json_structure_new_client =  "{"+f""""Nombre" : "{name}","Apellido" : "{apellido}", "correo": "{correo}", "duda":"{duda}" """ + "}" 
        json_data_new_client = json.loads(json_structure_new_client)
        nuevo_cliente = Cliente(per_primer_nombre = json_data_new_client['Nombre'],
                               per_primer_apellido = json_data_new_client['Apellido'], 
                               per_email = json_data_new_client['correo'])
        nuevo_cliente.save()
        nueva_duda = Consulta(con_cli_per_id = nuevo_cliente,
                              con_comentario = json_data_new_client['duda'])
        nueva_duda.save()
    except Exception as error: 
        messages.error(request, "La información no pudo ser enviada" + str(error))
    else:
        messages.success(request, "El dato ha sido ingresado con éxito")
    finally:
        return render(request, "main_dash/index.html")




