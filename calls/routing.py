#calls/routing.py
from django.urls import re_path
from .consumers import CallConsumer

websocket_urlpatterns = [
    re_path(r"ws/calls/call/(?P<caller_id>\d+)/(?P<receiver_id>\d+)/$", CallConsumer.as_asgi()),
]