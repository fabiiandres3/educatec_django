from django.shortcuts import render, redirect
from apps.calificaciones.models import Estudiante, Calificacion, Asistencia, Mensaje, Tarea, Docente
from django.utils import timezone

ESTUDIANTE_ID = 1

def get_estudiante():
    return Estudiante.objects.filter(id=ESTUDIANTE_ID).first()

def get_stats(estudiante):
    calificaciones = Calificacion.objects.filter(estudiante=estudiante)
    promedio_general = round(sum(c.promedio for c in calificaciones) / calificaciones.count(), 1) if calificaciones.exists() else 0
    asistencias = Asistencia.objects.filter(estudiante=estudiante)
    total_asis = asistencias.count()
    presentes = asistencias.filter(estado='presente').count()
    tardanzas = asistencias.filter(estado='tardanza').count()
    ausentes = asistencias.filter(estado='ausente').count()
    porcentaje_asistencia = round((presentes / total_asis) * 100) if total_asis > 0 else 0
    aprobadas = sum(1 for c in calificaciones if c.promedio >= 3.0)
    en_riesgo = sum(1 for c in calificaciones if c.promedio < 3.0)
    total_logros = sum([porcentaje_asistencia >= 90, promedio_general >= 4.5, promedio_general >= 3.0])
    return {
        'calificaciones': calificaciones,
        'promedio_general': promedio_general,
        'porcentaje_asistencia': porcentaje_asistencia,
        'presentes': presentes,
        'tardanzas': tardanzas,
        'ausentes': ausentes,
        'aprobadas': aprobadas,
        'en_riesgo': en_riesgo,
        'total_logros': total_logros,
    }

def dashboard_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/dashboard_alumno.html', {})
    stats = get_stats(estudiante)
    tareas = Tarea.objects.filter(curso=estudiante.curso)
    mensajes = Mensaje.objects.filter(estudiante=estudiante).order_by('-fecha')
    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()
    context = {
        'estudiante': estudiante,
        'tareas_pendientes': tareas.filter(estado='pendiente').count(),
        'mensajes_recientes': mensajes[:3],
        'mensajes_sin_leer': sin_leer,
        **stats,
    }
    return render(request, 'alumno/dashboard_alumno.html', context)

def materias_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/materias_alumno.html', {})
    stats = get_stats(estudiante)
    return render(request, 'alumno/materias_alumno.html', {'estudiante': estudiante, **stats})

def tareas_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/tareas_alumno.html', {})
    tareas = Tarea.objects.filter(curso=estudiante.curso).order_by('fecha_limite')
    context = {
        'estudiante': estudiante,
        'tareas': tareas,
        'total_tareas': tareas.count(),
        'pendientes': tareas.filter(estado='pendiente').count(),
        'entregadas': tareas.filter(estado='entregada').count(),
        'vencidas': tareas.filter(estado='vencida').count(),
    }
    return render(request, 'alumno/tareas_alumno.html', context)

def calificaciones_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/calificaciones_alumno.html', {})
    stats = get_stats(estudiante)
    return render(request, 'alumno/calificaciones_alumno.html', {'estudiante': estudiante, **stats})

def asistencia_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/asistencia_alumno.html', {})
    asistencias = Asistencia.objects.filter(estudiante=estudiante).order_by('-fecha')
    stats = get_stats(estudiante)
    return render(request, 'alumno/asistencia_alumno.html', {
        'estudiante': estudiante,
        'asistencias': asistencias,
        **stats,
    })

def mensajes_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/mensajes_alumno.html', {})
    mensajes = Mensaje.objects.filter(estudiante=estudiante).order_by('fecha')
    Mensaje.objects.filter(estudiante=estudiante, enviado_por='docente', leido=False).update(leido=True)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            docente = Docente.objects.filter(id=1).first()
            if docente:
                Mensaje.objects.create(
                    docente=docente, estudiante=estudiante,
                    contenido=contenido, enviado_por='estudiante'
                )
        return redirect('mensajes_alumno')
    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()
    enviados = mensajes.filter(enviado_por='estudiante').count()
    return render(request, 'alumno/mensajes_alumno.html', {
        'estudiante': estudiante,
        'mensajes': mensajes,
        'sin_leer': sin_leer,
        'enviados': enviados,
    })

def logros_alumno(request):
    estudiante = get_estudiante()

    if not estudiante:
        return render(
            request,
            'alumno/logros_alumno.html',
            {
                'promedio': 0,
                'porcentaje_asistencia': 0,
                'total_logros': 0,
                'logros_por_desbloquear': 5,
            }
        )

    stats = get_stats(estudiante)

    context = {
        'estudiante': estudiante,
        **stats,
    }

    return render(
        request,
        'alumno/logros_alumno.html',
        context
    )

def configuracion_alumno(request):
    estudiante = get_estudiante()
    return render(request, 'alumno/configuracion_alumno.html', {'estudiante': estudiante})