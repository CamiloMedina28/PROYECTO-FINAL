from django.shortcuts import render
import mysql.connector as db_connector
from django.contrib import messages


# Create your views here.

def index(request):
    return render (request, "main_dash/index.html")

def nosotros(request):
    return render(request, "main_dash/nosotros.html")

def productos(request):
    return render(request, "main_dash/productos.html")

def send_info(request):
    if request.method == "POST":
        name = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        duda = request.POST.get('duda')

    db_reg_info = db_connector.connect(
        host = "dorabisuteriadb.mysql.database.azure.com",
        user = "insert_info_con",
        password = "insert_123"
    )

    cursor = db_reg_info.cursor()
    cursor.execute("USE dora_bisuteria")
    cursor.execute("INSERT INTO persona(per_primer_nombre, per_primer_apellido, per_email)" "VALUES(%s,%s,%s)", (name, apellido, correo))
    cursor.execute("SELECT LAST_INSERT_ID();")
    ultimo_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO cliente(cli_per_id)" "VALUES(%s)", (ultimo_id,))
    cursor.execute("INSERT INTO consulta(con_cli_per_id, con_comentario)" "VALUES(%s,%s)", (ultimo_id, duda))

    db_reg_info.commit()

    messages.success(request, "La consulta ha sido enviada con éxito")
    return render (request, "main_dash/index.html")




