#!/usr/bin/env python
#-*- encoding: utf-8 -*-

PLUGINS = [
    'LogInfoPlugin',
    'EventPlugin',
]

# LogInfo Plugin Configuration
NO_PRINT_API = [
    'GetUser',
    'ListUsers',
    'AuthToken',
    'GetToken',
    'ExpireToken',
]

# Event Plugin Configuration
STORE_HOST = ''
EVENT_INFO = {
    'CreateUser': ('Create a user. (%s)', 'user_id'),
}
