import uuid
from django.db import models

class user(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=20, default='enable')
    email = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=30)
    timezone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class token(models.Model):
    user = models.ForeignKey('user', to_field='user_id')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
