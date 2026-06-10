from django import forms
from .models import Tareas, Pregunta, Respuesta


class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ["titulo", "descripcion", "video", "fecha_entrega"]


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["enunciado", "tipo"]


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ["respuesta_texto", "opcion_seleccionada"]


class VideoForm(forms.Form):
    url = forms.URLField(label="URL de YouTube")
