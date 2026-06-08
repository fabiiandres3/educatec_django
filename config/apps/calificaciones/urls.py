from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_notas, name='lista_notas'),
    path('guardar/', views.guardar_nota, name='guardar_nota'),
    path('editar/<int:id>/', views.editar_nota, name='editar_nota'),
    path('eliminar/<int:id>/', views.eliminar_nota, name='eliminar_nota'),
]