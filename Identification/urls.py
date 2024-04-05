from django.urls import path
from .views import select_state

urlpatterns = [
    path('species_by_state/', select_state, name='id_view'),
]