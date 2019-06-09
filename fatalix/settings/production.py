# -*- coding: utf-8 -*-
import os
from .common import *

DEBUG = False

with open('secret.txt') as f:
    SECRET_KEY = f.read().strip()


# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('/var/www/vhosts/fatalix.de/httpdocs', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('/var/www/vhosts/fatalix.de/httpdocs', 'media')
