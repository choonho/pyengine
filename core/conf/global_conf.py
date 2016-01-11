#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# Auth Settings
# API Auth Type : noauth | xauth
AUTH_TYPE = 'xauth'
AUTH_HOST = 'localhost'

NO_AUTH_MODULES = ['token']

SYSTEM_AUTH_MODULES = ['system']
SYSTEM_KEY = '816801afffe508cf99cb' 


# Default Settings
DEFAULT_LANGUAGE = 'ko'
DEFAULT_TIMEZONE = 'Asia/Seoul'

DEFAULT_JOB_TIMEOUT = 1800

TOKEN_EXPIRE_TIME = 86400

DATETIME_FIELDS = ['created', 'last_update', 'finished', 'deleted']
