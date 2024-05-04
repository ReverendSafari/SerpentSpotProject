from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), # path to login page
    path('register/', views.register_view, name='register'), # path to register page
    path('profile/', views.profile_view, name='profile'), # path to view user profile
    path('profile/<str:username>/', views.profile_view, name='user_profile'),  # path to view other users' profiles
    path('edit-profile/', views.edit_profile_view, name='edit_profile'), # path to edit user profile
    path('logout/', views.logout_view, name='logout'), # path to logout
] 