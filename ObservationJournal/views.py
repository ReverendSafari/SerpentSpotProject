from django.shortcuts import render

# Create your views here.
def journal_view(request):
    return render(request, 'observationjournal.html')