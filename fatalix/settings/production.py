# -*- coding: utf-8 -*-
import os
from .common import *

DEBUG = False

with open('secret.txt') as f:
    SECRET_KEY = f.read().strip()


# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
