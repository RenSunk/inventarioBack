from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(Rol)
admin.site.register(RolPermiso)
admin.site.register(Permiso)
