from django.contrib import admin
from .models import Partido

# Register your models here.
@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    readonly_fields = ('createdP', 'modifiedP')  # Campos solo lectura en el panel de admin
    list_display = ('equipo_1', 'equipo_2', 'fecha', 'hora', 'createdP', 'modifiedP')  # Columnas visibles en la lista
    date_hierarchy = 'createdP'  # Navegación por fechas en el panel