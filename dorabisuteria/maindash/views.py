from django.shortcuts import render
import mysql.connector as db_connector

# Create your views here.

def index(request):
    return render (request, "main_dash/index.html")

def register_form_data(request):
    db_reg_info = db_connector.connect(
        host = "dorabisuteriadb.mysql.database.azure.com",
        user = "",
        password =""
    )





