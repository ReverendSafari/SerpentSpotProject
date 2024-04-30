from Identification.models import State, SnakeSpecies
from django.shortcuts import render


from django.shortcuts import render
from .models import State, SnakeSpecies

def select_state(request):
    selected_state_name = "the USA"
    species_qs = SnakeSpecies.objects.all()  # Start with all species

    # Get the search term from the GET request
    search_term = request.GET.get('search', '')
    selected_state_id = request.GET.get('state')  # Use GET instead of POST

    # Filter your species by the search term if it's not empty
    if search_term:
        species_qs = species_qs.filter(common_name__icontains=search_term)

    # Filter by selected state if provided
    if selected_state_id:
        try:
            selected_state = State.objects.get(id=selected_state_id)
            selected_state_name = selected_state.name
            species_qs = species_qs.filter(states__id=selected_state_id)
        except State.DoesNotExist:
            # If the state doesn't exist, reset to the USA view without filtering by state
            selected_state_name = "the USA"
            selected_state_id = None
    # Get the species data for the template
    species_data = [
        {
            'common_name': s.common_name, # Include common name
            'scientific_name': s.scientific_name, # Include scientific name
            'description': s.description, # Include description
            'venomous': s.venomous, # Include venomous status
            'image_path': s.image_path, # Get the image path
            'states': s.states.all(), # Get all states where snake is present
        }
        for s in species_qs
    ]

    # Get all states for the dropdown
    states = State.objects.all()
    species_count = species_qs.count()


    species_data = []
    for s in species_qs:
        species_data.append({
            'common_name': s.common_name,
            'scientific_name': s.scientific_name,
            'description': s.description,
            'venomous': s.venomous,
            'image_path': s.image_path,
        })
    
    

    context = {
        'states': states,
        'species': species_data,
        'selected_state_name': selected_state_name,
        'species_count': species_count,
    }

    return render(request, 'id.html', context)


def render_education(request):
    return render(request, 'education.html')