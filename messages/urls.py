from django.urls import path
from . import views


urlpatterns = [
    path("messages/", views.messages, name="messages"),
    path("messages/<int:user_id>/", views.message, name="message"),
    ]