from django.conf.urls import include, url
from core.views import Core

urlpatterns = [
    url(r'^core/.*', Core.as_view()),
]
