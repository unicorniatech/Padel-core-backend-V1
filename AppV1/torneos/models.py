from django.db import models

# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(max_length=255)
    sede = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    premio_dinero = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,verbose_name="Premio ($)")  # Valor predeterminado: 0.00
    createdT = models.DateTimeField(auto_now_add=True,verbose_name="Creado") #Para saber cuanto tiempo lleva Creado
    modifiedT = models.DateTimeField(auto_now=True, verbose_name="Modificado") #Para saber última modificación

    def __str__(self):
        return f"{self.nombre} - {self.sede} ({self.fecha_inicio} - {self.fecha_fin})"
    