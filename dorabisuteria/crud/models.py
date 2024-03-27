from django.db import models

# Create your models here.


class Persona(models.Model):
    per_id = models.AutoField(primary_key=True)
    per_primer_nombre = models.CharField("Person's first name", max_length=50)
    per_segundo_nombre = models.CharField("Person's second name", max_length = 50, blank =True, null = True)
    per_primer_apellido = models.CharField("Person's first last name", max_length=50)
    per_segundo_apellido = models.CharField("Person's second last name", max_length=50, blank =True, null = True)
    per_email = models.EmailField("Person's email")
    per_telefono = models.PositiveBigIntegerField("person's phone number", blank = True, null = True)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

class Cliente(Persona):

    class Meta: 
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Empleado(Persona):
    emp_cedula = models.PositiveIntegerField("Employee's id", primary_key = True)
    emp_cargo = models.CharField("Employee's job", max_length = 50 ,blank =  True, null = True)
    emp_salario = models.PositiveIntegerField("Employee's salary", blank = True, null = True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

class Consulta(models.Model):
    con_cli_per_id = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    con_comentario = models.CharField("Client's comment",max_length = 150)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "EConsultas"

class Proveedor(models.Model):
    prov_nit = models.BigIntegerField(primary_key = True)
    prov_razon_social = models.CharField("Razón social del proveedor", max_length = 50)
    prov_telefono = models.BigIntegerField("Teléfono del proveedor")

class Material(models.Model):
    mat_id = models.AutoField(primary_key= True)
    mat_prov_id = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
    stock = models.IntegerField()
    nombre = models.CharField("Nombre del material ", max_length = 50)

class Producto(models.Model):
    pro_id = models.IntegerField(primary_key = True)
    pro_nombre = models.CharField("Nombre del producto", max_length = 50)
    pro_precio = models.IntegerField("Precio del producto")
    pro_stock = models.IntegerField("Stock del producto")
    pro_img = models.ImageField(upload_to='static/img/EDITADAS/nuevas')
    materiales = models.ManyToManyField(Material)