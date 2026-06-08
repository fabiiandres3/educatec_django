from django.db import models

class Nota(models.Model):
    estudiante = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.materia}: {self.calificacion}"
