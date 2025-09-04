from django.urls import path
from . import views

#
app_name = 'core'  #✅ This enables namespace

urlpatterns = [
    path("", views.feed, name="feed"),

]
