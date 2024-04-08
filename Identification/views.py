from django.shortcuts import render, redirect
from .models import State, SnakeSpecies

def select_state(request):
    states = State.objects.all()
    species = []
    if request.method == 'POST':
        selected_state_id = request.POST.get('state')
        species = SnakeSpecies.objects.filter(states__id=selected_state_id)
    
    return render(request, 'id.html', {
        'states': states,
        'species': species,
    })

def render_education(request):
    return render(request, 'education.html')