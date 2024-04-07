from django.urls import path
from .views import select_state, render_education

urlpatterns = [
    path('id/', select_state, name='id_view'),
    path('education/', render_education, name='education_view')
]