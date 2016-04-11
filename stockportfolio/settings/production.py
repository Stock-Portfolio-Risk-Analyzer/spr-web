from stockportfolio.settings.base import *

import os
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('SPARKPOST_SMTP_HOST')
EMAIL_PORT = os.environ.get('SPARKPOST_SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('SPARKPOST_SMTP_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SPARKPOST_SMTP_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Stock Portfolio <django-sparkpost@sparkpostbox.com>'
