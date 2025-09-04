from django.urls import path
from . import views
#posts/urls.py
app_name = 'posts'
urlpatterns = [
    # HTML Views

    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('search/', views.user_search, name='user_search'),

    # API endpoints (function-based)
    path('api/posts/', views.posts_api, name='api-posts'),
    path('api/posts/<int:post_id>/comment/', views.comment_api, name='api-comment'),
]
