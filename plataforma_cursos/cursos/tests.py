from django.test import TestCase
from django.contrib.auth import get_user_model  # Usamos get_user_model para obtener el modelo de usuario correcto
from .models import Curso, Progreso

User = get_user_model()

class CursoModelTest(TestCase):

    def setUp(self):
        # Crea un curso de prueba
        self.curso = Curso.objects.create(
            nombre="Curso de Python",
            descripcion="Un curso completo de Python.",
            total_paginas=120
        )

    def test_curso_creation(self):
        """Verifica que el curso se crea correctamente."""
        self.assertEqual(self.curso.nombre, "Curso de Python")
        self.assertEqual(self.curso.descripcion, "Un curso completo de Python.")
        self.assertEqual(self.curso.total_paginas, 120)

    def test_curso_string_representation(self):
        """Verifica la representación en cadena (str) del curso."""
        self.assertEqual(str(self.curso), "Curso de Python")


class ProgresoModelTest(TestCase):

    def setUp(self):
        # Crea un usuario y un curso de prueba
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.curso = Curso.objects.create(
            nombre="Curso de Django",
            descripcion="Aprende Django desde cero.",
            total_paginas=100  # Total de páginas en el curso
        )
        # Crea un progreso para ese curso
        self.progreso = Progreso.objects.create(
            usuario=self.usuario,
            curso=self.curso,
            paginas_visitadas=50,
            checks_alcanzados=30,
            examen_realizado=True,
            resultado_examen=80
        )

    def test_avance_total(self):
        """Verifica que el avance total se calcula correctamente."""
        # Avance total esperado:
        # Avance en páginas: (50/100) * 0.7 = 0.35
        # Resultado del examen: (80/100) * 0.3 = 0.24
        # Avance total = 0.35 + 0.24 = 0.59
        self.assertEqual(self.progreso.avance_total(), 0.59)

    def test_progreso_string_representation(self):
        """Verifica la representación en cadena (str) del progreso."""
        self.assertEqual(str(self.progreso), f"{self.usuario.username} - {self.curso.nombre}")


class UsuarioModelTest(TestCase):

    def setUp(self):
        # Crea un usuario de prueba
        self.usuario = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_usuario_creation(self):
        """Verifica que el usuario se crea correctamente."""
        self.assertEqual(self.usuario.username, "testuser")
        self.assertEqual(self.usuario.email, "testuser@example.com")

    def test_usuario_authentication(self):
        """Verifica que el usuario puede autenticarse con su contraseña."""
        self.assertTrue(self.usuario.check_password("password123"))