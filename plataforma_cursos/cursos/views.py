from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Curso, Progreso
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import UserRegistrationForm,CustomLoginForm
from django.http import JsonResponse
from django.http import HttpResponse
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('listado_cursos')  # Redirige a la página de inicio o al dashboard
    else:
        form = CustomLoginForm()
    return render(request, 'cursos/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al inicio de sesión o a otra página
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'total_paginas', 'imagen']

def registro_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_cursos')
    else:
        form = CursoForm()
    
    return render(request, 'cursos/registro_curso.html', {'form': form})




@login_required
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    progreso, created = Progreso.objects.get_or_create(usuario=request.user, curso=curso)

    contexto = {
        'curso': curso,
        'progreso': progreso,
    }
    return render(request, 'cursos/detalle_curso.html', contexto)


@login_required
def actualizar_progreso(request, curso_id):
    if request.method == 'POST':
        paginas_visitadas = int(request.POST.get('paginas_visitadas', 0))
        checks_alcanzados = int(request.POST.get('checks_alcanzados', 0))
        resultado_examen = float(request.POST.get('resultado_examen', 0))

        curso = get_object_or_404(Curso, id=curso_id)
        progreso = Progreso.objects.get(usuario=request.user, curso=curso)
        progreso.paginas_visitadas = paginas_visitadas
        progreso.checks_alcanzados = checks_alcanzados
        progreso.resultado_examen = resultado_examen
        progreso.examen_realizado = True
        progreso.save()

        return redirect('detalle_curso', curso_id=curso.id)
    

@login_required
def listado_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/listado_cursos.html', {'cursos': cursos})

@login_required
def registro_curso(request):
    form = CursoForm(request.POST, request.FILES) # Incluir request.FILES para manejar imágenes
    if form.is_valid():
        form.save()
        return redirect('listado_cursos')
    return render(request, 'cursos/registro_curso.html', {'form': form})

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Obtener el progreso del usuario en este curso, si existe
    progreso = None
    if request.user.is_authenticated:
        progreso = Progreso.objects.filter(usuario=request.user, curso=curso).first()

    context = {
        'curso': curso,
        'progreso': progreso,
    }
    return render(request, 'cursos/detalle_curso.html', context)

def homepage(request):
    return render(request, 'cursos/homepage.html')

# Algoritmo Quicksort para ordenar de mayor a menor
def quicksort(arr, key=None):
    if len(arr) <= 1:
        return arr
    pivot = key(arr[len(arr) // 2]) if key else arr[len(arr) // 2]
    
    left = [x for x in arr if key(x) < pivot] if key else [x for x in arr if x < pivot]
    middle = [x for x in arr if key(x) == pivot] if key else [x for x in arr if x == pivot]
    right = [x for x in arr if key(x) > pivot] if key else [x for x in arr if x > pivot]
    
    return quicksort(left, key=key) + middle + quicksort(right, key=key)

def listado_cursos_ordenados(request):
    cursos = Curso.objects.all()  # Obtén todos los cursos de la BD

    ordenar = request.GET.get('ordenar', 'false')  # Inicialmente desordenado

    if ordenar == 'true':
        cursos = quicksort(list(cursos), key=lambda curso: curso.total_paginas)  # Aplica el algoritmo quicksort
        cursos.reverse()  # Invierte el resultado para que sea descendente
    else:
        cursos = list(cursos)  # Mantiene el orden de la BD

    return render(request, 'cursos/listado_cursos_ordenados.html', {'cursos': cursos, 'ordenar': ordenar})

def metrics(request):
    registry = CollectorRegistry()
    # Esto recoge las métricas desde el registro por defecto
    metrics_page = generate_latest(registry)
    return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)