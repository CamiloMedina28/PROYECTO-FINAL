from django.contrib import admin
from .models import Persona
from .models import Cliente
from .models import Empleado
from .models import Consulta
from .models import Proveedor
from .models import Producto
from .models import Material

# Register your models here.

admin.site.register(Persona)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Consulta)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Material)



