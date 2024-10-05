import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_cursos.settings')  # Cambia 'plataforma_cursos' por el nombre de tu proyecto

application = get_wsgi_application()
# add this vercel variable
app = application
