from django.db import models
from embed_video.fields import EmbedVideoField


class Tareas(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    video = EmbedVideoField()
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Pregunta(models.Model):
    TIPOS = [
        ("abierta", "Respuesta abierta"),
        ("opcion_multiple", "Opción múltiple"),
    ]

    recurso_tarea = models.ForeignKey(
        Tareas, on_delete=models.CASCADE, related_name="preguntas"
    )
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    orden = models.PositiveIntegerField(default=1)


class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(
        Pregunta, on_delete=models.CASCADE, related_name="opciones"
    )
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta_texto = models.TextField(blank=True, null=True)
    opcion_seleccionada = models.ForeignKey(
        OpcionRespuesta, on_delete=models.SET_NULL, blank=True, null=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
