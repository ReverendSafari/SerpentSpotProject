from django.urls import path
from . import views

# @ Safari
# Simple URL pattern to display the map view

urlpatterns = [
    path('map_view', views.map_view, name='map_view'), 
]