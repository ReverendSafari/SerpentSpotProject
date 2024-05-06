from django.urls import path
from . import views

urlpatterns = [
   path('', views.faq_home, name='faq_home'),  # Assuming this is the main FAQ page
   path('<slug:slug>/', views.faq_detail, name='faq_detail'),  # This line is new
]
