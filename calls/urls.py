from django.urls import path
#call/urls.py
from . import views

urlpatterns = [

    path("video-call/", views.video_call, name="video_call"),

    ]