from Identification.models import State, SnakeSpecies
from django.shortcuts import render


from django.shortcuts import render
from .models import State, SnakeSpecies

def select_state(request):
    selected_state_name = "the USA"
    species = SnakeSpecies.objects.all()  # Default species list for no state selected

    selected_state_id = request.GET.get('state')  # Use GET instead of POST
    if selected_state_id:
        try:
            selected_state = State.objects.get(id=selected_state_id)
            selected_state_name = selected_state.name
            species = SnakeSpecies.objects.filter(states__id=selected_state_id)
        except State.DoesNotExist:
            # Handle the case where the state does not exist
            species = SnakeSpecies.objects.all()

    states = State.objects.all()

    species_data = []
    for s in species:
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
    }

    return render(request, 'id.html', context)


def render_education(request):
    return render(request, 'education.html')