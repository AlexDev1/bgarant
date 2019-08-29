from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'amv@9yy8m#1o0@3^965$c#g%5#7p)$jnr7)silwm#r(!_xaroq'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['garant-bisness.ru']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
