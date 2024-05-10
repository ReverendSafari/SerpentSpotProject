from django.shortcuts import render

# Seamus 
def home_view(request):
    return render(request, 'homepage.html') # Render the home.html template