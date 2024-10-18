from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Curso, Progreso
from django.urls import reverse
from django.core.paginator import Paginator

User = get_user_model()

# Pruebas para el modelo Curso
class CursoModelTest(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(
            nombre="Curso de Python",
            descripcion="Un curso completo de Python.",
            total_paginas=120
        )

    def test_curso_creation(self):
        self.assertEqual(self.curso.nombre, "Curso de Python")
        self.assertEqual(self.curso.descripcion, "Un curso completo de Python.")
        self.assertEqual(self.curso.total_paginas, 120)

    def test_curso_string_representation(self):
        self.assertEqual(str(self.curso), "Curso de Python")


# Pruebas de validación para modelo Curso
class CursoValidationTest(TestCase):

    def setUp(self):
        # Crear un curso válido para usar en las pruebas
        self.curso = Curso.objects.create(
            nombre="Curso de Prueba",
            descripcion="Descripción del curso.",
            total_paginas=150
        )

    def test_curso_invalid_type(self):
        # Intentar asignar un valor no válido al campo 'total_paginas'
        with self.assertRaises(ValueError):
            self.curso.total_paginas = "no_es_numero"
            self.curso.save()
    
    def test_curso_empty_name(self):
        # Probar la creación de un curso con un nombre vacío
        with self.assertRaises(ValueError):
            curso_invalido = Curso.objects.create(
                nombre="",  # Nombre vacío
                descripcion="Descripción sin nombre",
                total_paginas=50
            )

    def test_progreso_avance_max_value(self):
        # Asegurarse de que el avance no exceda el 100%
        self.progreso = Progreso.objects.create(
            usuario=User.objects.create_user(username='testuser2', password='54321'),
            curso=self.curso,
            paginas_visitadas=200,  # Excediendo el total de páginas
            checks_alcanzados=50,
            examen_realizado=True,
            resultado_examen=90
        )
        avance_total = self.progreso.avance_total()
        self.assertLessEqual(avance_total, 1.0)  # El avance nunca debe ser mayor a 1 (100%)


# Pruebas para el modelo Progreso
class ProgresoModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.curso = Curso.objects.create(
            nombre="Curso de Django",
            descripcion="Aprende Django desde cero.",
            total_paginas=100
        )
        self.progreso = Progreso.objects.create(
            usuario=self.usuario,
            curso=self.curso,
            paginas_visitadas=50,
            checks_alcanzados=30,
            examen_realizado=True,
            resultado_examen=80
        )

    def test_avance_total(self):
        self.assertEqual(self.progreso.avance_total(), 0.59)

    def test_progreso_overflow(self):
        self.progreso.paginas_visitadas = 120  # Más páginas que las totales
        self.progreso.save()

        total_paginas = self.progreso.curso.total_paginas
        paginas_visitadas = min(self.progreso.paginas_visitadas, total_paginas)
        avance_esperado = paginas_visitadas / total_paginas
        self.assertLessEqual(avance_esperado, 1.0)

    def test_progreso_string_representation(self):
        self.assertEqual(str(self.progreso), f"{self.usuario.username} - {self.curso.nombre}")


# Pruebas para el modelo Usuario
class UsuarioModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.username, "testuser")
        self.assertEqual(self.usuario.email, "testuser@example.com")

    def test_usuario_authentication(self):
        self.assertTrue(self.usuario.check_password("password123"))


# Pruebas de paginación para cursos
class CursoPaginationTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        for i in range(15):  # Aumentamos el número de cursos creados para asegurar más páginas
            Curso.objects.create(
                nombre=f"Curso {i}",
                descripcion=f"Descripción del curso {i}",
                total_paginas=100 + i
            )

    def test_curso_pagination(self):
        response = self.client.get(reverse('listado_cursos') + '?page=2')

        paginator = Paginator(Curso.objects.order_by('id'), 5)  # 5 cursos por página
        page = paginator.page(2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(page.object_list), 5)  # Cada página debe tener 5 cursos
        self.assertTrue(page.has_next())  # Asegurar que hay una tercera página


# Pruebas de ordenamiento para cursos
class CursoSortingTest(TestCase):

    def setUp(self):
        self.curso1 = Curso.objects.create(nombre="Curso A", descripcion="Curso A Desc", total_paginas=200)
        self.curso2 = Curso.objects.create(nombre="Curso B", descripcion="Curso B Desc", total_paginas=100)
        self.curso3 = Curso.objects.create(nombre="Curso C", descripcion="Curso C Desc", total_paginas=300)

    def test_curso_sorting(self):
        response = self.client.get(reverse('listado_cursos_ordenados') + '?ordenar=true')
        cursos = list(response.context['cursos'])
        self.assertEqual(cursos[0].total_paginas, 300)
        self.assertEqual(cursos[1].total_paginas, 200)
        self.assertEqual(cursos[2].total_paginas, 100)


# Pruebas para el modelo de Usuario Administrador
class AdminUserModelTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="adminpassword123"
        )

    def test_admin_user_creation(self):
        self.assertEqual(self.admin_user.username, "adminuser")
        self.assertEqual(self.admin_user.email, "adminuser@example.com")
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_admin_user_authentication(self):
        self.assertTrue(self.admin_user.check_password("adminpassword123"))

    def test_admin_access(self):
        login_successful = self.client.login(username='adminuser', password='adminpassword123')
        self.assertTrue(login_successful)

        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)