from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Curso, CustomUser, Progreso

class CustomUserAdmin(UserAdmin):
    model = CustomUser

admin.site.register(Curso)
admin.site.register(Progreso)

admin.site.register(CustomUser, CustomUserAdmin)

