from django.shortcuts import render, get_object_or_404, redirect
from .models import Nota
from .forms import NotaForm

def lista_notas(request):
    notas = Nota.objects.all()
    form = NotaForm()
    return render(request, 'calificaciones/index.html', {'notas': notas, 'form': form})

def guardar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('lista_notas')

def editar_nota(request, id):
    nota = get_object_or_404(Nota, id=id)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('lista_notas')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'calificaciones/editar.html', {'form': form, 'nota': nota})

def eliminar_nota(request, id):
    nota = get_object_or_404(Nota, id=id)
    nota.delete()
    return redirect('lista_notas')