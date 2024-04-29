from django.shortcuts import render, get_object_or_404
from .models import FAQ  # Make sure to import your FAQ model

# This view will handle the display of the FAQ list on the home page
def faq_home(request):
    faqs = FAQ.objects.all()  # Retrieve all FAQ objects from the database
    return render(request, 'faq_home.html', {'faqs': faqs})

# This view will handle the display of a specific FAQ based on the slug
def faq_detail(request, slug):
    faq = get_object_or_404(FAQ, slug=slug)  # Retrieve the specific FAQ object or return a 404 error
    return render(request, 'faq_detail.html', {'faq': faq})
