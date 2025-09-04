from django.urls import path
from . import views

app_name = "calls"

urlpatterns = [
    path("video/<int:receiver_id>/", views.video_call, name="video_call"),
]
