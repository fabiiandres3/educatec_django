from django.urls import path
from . import views

urlpatterns = [
    path('tareas/', views.listar_tareas, name='listar_tareas'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('reproductor/', views.reproductor, name='reproductor'),
    path('subir_imagen/', views.subir_imagen, name='subir_imagen'),
    path('detalle/tarea/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    path("tarea/<int:tarea_id>/responder/", views.responder_tarea, name="responder_tarea"),
]