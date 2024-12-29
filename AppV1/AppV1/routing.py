from django.urls import re_path #Esto maneja URLs
from . import consumer

websecket_urlpatterns = [
    re_path(r'ws/jugadores/$',consumer.MyConsumer.as_asgi()),
]

