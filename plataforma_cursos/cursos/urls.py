from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', register, name='register'),
    path('listado/', views.listado_cursos, name='listado_cursos'),
    path('registro_curso/', views.registro_curso, name='registro_curso'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('<int:curso_id>/actualizar/', views.actualizar_progreso, name='actualizar_progreso')    
]