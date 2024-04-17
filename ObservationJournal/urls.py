from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_view, name='journal_view'),
    path('<str:username>/', views.journal_view, name='user_journal_view'),
    path('delete/<int:observation_id>/', views.delete_observation, name='delete_observation'),
]