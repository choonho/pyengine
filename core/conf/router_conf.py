#!/usr/bin/env python
#-*- encoding: utf-8 -*-

MODULE = 'compute'
URL_PREFIX = '/core'

URLS = [
    # Example: (sub_module, path, method, api_class), 

    # User Module
    ('user', '/{api_version:v1}/users', 'POST', 'CreateUser'),  
    ('user', '/{api_version:v1}/user/{user_id}', 'PUT', 'UpdateUser'),  
    ('user', '/{api_version:v1}/user/{user_id}', 'DELETE', 'DeleteUser'),  
    ('user', '/{api_version:v1}/user/{user_id}/enable', 'POST', 'EnableUser'),  
    ('user', '/{api_version:v1}/user/{user_id}/disable', 'POST', 'DisableUser'),  
    ('user', '/{api_version:v1}/user/{user_id}', 'GET', 'GetUser'),  
    ('user', '/{api_version:v1}/users', 'GET', 'ListUsers'),  
    ('user', '/{api_version:v1}/users/filter', 'POST', 'ListUsers'),  

    # Token Module
    ('token', '/{api_version:v1}/token/get', 'POST', 'GetToken'),
    ('token', '/{api_version:v1}/token/expire', 'POST', 'ExpireToken'),  

    # System Module
    ('system', '/{api_version:v1}/token/auth', 'GET', 'AuthToken'),  

]
