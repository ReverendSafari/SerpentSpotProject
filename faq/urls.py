from django.urls import path
from . import views

# @Safari
# URL patterns for the FAQ app
# The first URL pattern is for the main FAQ page, which will list all the FAQs
# The second URL pattern is for a specific FAQ, which will display the FAQ details
urlpatterns = [
   path('', views.faq_home, name='faq_home'),  # Assuming this is the main FAQ page
   path('<slug:slug>/', views.faq_detail, name='faq_detail'),  # This line is new
]
