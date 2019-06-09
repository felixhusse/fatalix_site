# -*- coding: utf-8 -*-
from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mo(cx$^@%ao&pk(7#a28zy-d+6^cv5k&&i#(9r6bnb!cp+8kut'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
