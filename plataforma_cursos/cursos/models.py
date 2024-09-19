from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    total_paginas = models.IntegerField()
    imagen = models.ImageField(upload_to='cursos_imagenes/', blank=True, null=True)  # Campo para la imagen

    def __str__(self):
        return self.nombre


class Progreso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    paginas_visitadas = models.IntegerField(default=0)
    checks_alcanzados = models.IntegerField(default=0)
    examen_realizado = models.BooleanField(default=False)
    resultado_examen = models.FloatField(null=True, blank=True)

    def avance_total(self):
        peso_avance = 0.7
        peso_examen = 0.3

        avance = (self.paginas_visitadas / self.curso.total_paginas) * peso_avance
        resultado_examen = (self.resultado_examen / 100) * peso_examen if self.resultado_examen else 0

        return round(avance + resultado_examen, 2)

    def __str__(self):
        return f'{self.usuario} - {self.curso.nombre}'