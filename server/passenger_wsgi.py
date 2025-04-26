import os, sys
sys.path.insert(0, '/home/v/varavkf7/varavkf7.beget.tech/secondlife')
sys.path.insert(1, '/home/v/varavkf7/varavkf7.beget.tech/djvenv/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'secondlife.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()