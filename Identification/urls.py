from django.urls import path
from .views import select_state, render_education

# @Safari
# Simple URL patterns, one for the id page and one for the education page
urlpatterns = [
    path('id/', select_state, name='id_view'),
    path('education/', render_education, name='education_view')
]