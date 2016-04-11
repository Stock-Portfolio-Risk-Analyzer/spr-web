from stockportfolio.settings.base import *

INSTALLED_APPS += (
    'django_nose',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=stockportfolio',
    '--cover-branches',
]
