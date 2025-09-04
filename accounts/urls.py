from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),

    # API endpoints
    path('api/signup/', views.signup_api, name='api-signup'),
    path('api/login/', views.login_api, name='api-login'),
    path('api/profile/<int:user_id>/', views.user_profile_api, name='api-profile'),
    path('api/follow/<int:user_id>/', views.follow_user_api, name='api-follow'),
    path('api/unfollow/<int:user_id>/', views.unfollow_user_api, name='api-unfollow'),

]
