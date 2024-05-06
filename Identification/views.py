from Identification.models import State, SnakeSpecies
from django.shortcuts import render


from django.shortcuts import render
from .models import State, SnakeSpecies

def select_state(request):
    selected_state_name = "the USA"
    species_qs = SnakeSpecies.objects.all()  # Start with all species

    # Get the search term and selected state ID from the GET request
    search_term = request.GET.get('search', '')
    selected_state_id = request.GET.get('state')

    # Filter the species by the search term if it's not empty
    if search_term:
        species_qs = species_qs.filter(common_name__icontains=search_term)

    # Filter by selected state if provided
    if selected_state_id:
        try:
            selected_state = State.objects.get(id=selected_state_id)
            selected_state_name = selected_state.name
            species_qs = species_qs.filter(states__id=selected_state_id)
        except State.DoesNotExist:
            selected_state_name = "the USA"
            selected_state_id = None

    species_data = [
        {
            'common_name': s.common_name,
            'scientific_name': s.scientific_name,
            'description': s.description,
            'venomous': s.venomous,
            'image_path': s.image_path,
            'states': [state.name for state in s.states.all()],
        }
        for s in species_qs
    ]

    # Prepare all states for the dropdown
    states = State.objects.all()
    species_count = species_qs.count() # Count the number of species

    context = {
        'states': states,
        'species': species_data,
        'selected_state_name': selected_state_name,
        'species_count': species_count,
        'search_term': search_term,
    }

    return render(request, 'id.html', context)

def render_education(request):
    return render(request, 'education.html')