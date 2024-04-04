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

    def __str__(self) -> str:
        texto = "id: {0} - nombre: {1} - apellido: {2}"
        return  texto.format(self.per_id, self.per_primer_nombre, self.per_primer_apellido)

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

    def __str__(self) -> str:
        texto = "cédula: {0} - nombre: {1} - apellido: {2} - cargo: {3}"
        return texto.format(self.per_id, self.per_primer_nombre, self.per_primer_apellido, self.emp_cargo)

class Consulta(models.Model):
    con_cli_per_id = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    con_comentario = models.CharField("Client's comment",max_length = 150)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self) -> str:
        texto = "id: {0} - consulta: {3}"
        return texto.format(self.con_cli_per_id, self.con_comentario)

class Proveedor(models.Model):
    prov_nit = models.BigIntegerField(primary_key = True)
    prov_razon_social = models.CharField("Razón social del proveedor", max_length = 50)
    prov_telefono = models.BigIntegerField("Teléfono del proveedor")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self) -> str:
        texto = "nit: {0} - razón social: {1}"
        return texto.format(self.prov_nit, self.prov_razon_social)

class Material(models.Model):
    mat_id = models.AutoField(primary_key= True)
    mat_prov_id = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
    stock = models.IntegerField()
    nombre = models.CharField("Nombre del material ", max_length = 50)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def __str__(self) -> str:
        texto = "id: {0} - proveedor: {1} - stock: {2} - nombre:{3}"
        return texto.format(self.mat_id, self.mat_prov_id, self.stock, self.nombre)

class Producto(models.Model):
    pro_id = models.IntegerField(primary_key = True)
    pro_nombre = models.CharField("Nombre del producto", max_length = 50)
    pro_precio = models.IntegerField("Precio del producto")
    pro_stock = models.IntegerField("Stock del producto")
    pro_img = models.ImageField(upload_to='products/')
    materiales = models.ManyToManyField(Material)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self) -> str:
        texto = "id_proveedor: {0} - id_material: {1} - nombre: {2} - precio: {3}"
        return texto.format(self.pro_id, self.materiales, self.pro_nombre, self.pro_precio)