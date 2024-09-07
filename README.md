# Plataforma de Cursos - Django Web Application

Este proyecto es una plataforma web para gestionar cursos de tecnología. Los usuarios pueden registrarse, iniciar sesión, ver un listado de cursos, registrar nuevos cursos, y seguir su progreso.

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.8+ ([Descargar Python](https://www.python.org/downloads/))
- pip (administrador de paquetes de Python)
- virtualenv (opcional, pero recomendado para aislar las dependencias)

## Instalación

### 1. Clonar el repositorio

Clona este repositorio a tu máquina local:

```bash
git clone https://github.com/usuario/plataforma-cursos.git
cd plataforma-cursos
```

### 2. Crear y activar un entorno virtual

En Windows:

```bash
python3 -m venv env
env\Scripts\activate
```
En macOS / Linux:

```bash
python3 -m venv env
source env/bin/activate
```
### 3. Instalar dependencias

```bash
pip3 install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
python3 manage.py migrate
```


### 5. Crear un superusuario

```bash
python3 manage.py createsuperuser
```

Sigue las instrucciones para configurar el nombre de usuario, email, y contraseña.

### 6. Correr el servidor de desarrollo

```bash
python manage.py runserver
```

Accede a la aplicación en tu navegador en http://127.0.0.1:8000.

Funcionalidades

	•	Registro de usuarios
	•	Iniciar sesión y cerrar sesión
	•	Listado de cursos
	•	Registrar nuevos cursos
	•	Administrar los cursos a través del panel de administración de Django en http://127.0.0.1:8000/admin/

Estructura de carpetas
```bash
plataforma_cursos/
├── cursos/                   # Aplicación de Django para manejar los cursos
│   ├── migrations/           # Migraciones de la base de datos
│   ├── static/               # Archivos estáticos (CSS, JavaScript, imágenes)
│   ├── templates/            # Plantillas HTML
│   ├── admin.py              # Registro de modelos en el administrador
│   ├── models.py             # Definición de los modelos
│   ├── views.py              # Lógica de las vistas
│   ├── urls.py               # Rutas de la aplicación
├── plataforma_cursos/        # Configuración global del proyecto Django
│   ├── settings.py           # Configuración general de Django
│   ├── urls.py               # URLs principales del proyecto
├── manage.py                 # Script principal para administrar el proyecto
├── requirements.txt          # Lista de dependencias del proyecto
└── README.md                 # Este archivo con instrucciones
```

Notas

	•	Panel de Administración: Accede al panel de administración en http://127.0.0.1:8000/admin/ con el superusuario que creaste.
	•	Modificaciones a la configuración: Puedes ajustar la configuración de la base de datos o cualquier otro parámetro en plataforma_cursos/settings.py.

