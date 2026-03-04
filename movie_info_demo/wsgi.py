import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_info_demo.settings')


application = get_wsgi_application()