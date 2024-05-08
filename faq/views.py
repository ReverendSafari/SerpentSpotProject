from django.shortcuts import render, get_object_or_404
from .models import FAQ  # Make sure to import your FAQ model

#
# @ Safari
# 
# Resources used:
# (Inspo) https://help.fabletics.com/hc/en-us/sections/360007879392-Membership
# (Inspo) https://www.zendesk.com/blog/the-best-faq-page-examples-and-how-to-make-your-own/
# https://learndjango.com/tutorials/django-slug-tutorial


"""
Handles the display of the FAQ list on the home page.

Args:
    request: The request object.

Returns:
    render object: The render object for the FAQ list on the home page. (Include all faq objects)

"""
def faq_home(request):
    faqs = FAQ.objects.all()  # Retrieve all FAQ objects from the database
    return render(request, 'faq_home.html', {'faqs': faqs})


"""
Handles the display of a specific FAQ based on the slug.

Args:
    request: The request object.

Returns:
    render object: The render object for the specific FAQ page. (Include the specific FAQ object)

"""
def faq_detail(request, slug):
    faq = get_object_or_404(FAQ, slug=slug)  # Retrieve the specific FAQ object or return a 404 error
    return render(request, 'faq_detail.html', {'faq': faq})
