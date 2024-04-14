from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from Identification.models import SnakeSpecies, State

from .models import UserObservation
from .forms import ObservationForm

# Create your views here.
def journal_view(request):
    species = SnakeSpecies.objects.all()  # Get all snake species
    if request.method == 'POST':
        form = ObservationForm(request.POST, request.FILES) # Create a form instance with POST data
        if form.is_valid(): # Check if the form data is valid
            observation = form.save(commit=False) # Create, but don't save the new observation object
            observation.species = form.cleaned_data['species'] # Set the species of the observation
            observation.user = request.user.userprofile  # Link the observation to the current user
            observation.save() # Save the observation object
            observation.user.observations += 1  # Increment observation count 
            observation.user.save()
            return redirect('journal_view')  # Redirect to avoid re-posting
    else: # If the form has not been submitted
        form = ObservationForm() # Create an empty form

    observations = UserObservation.objects.all()  # Get all observations
    observations = observations.filter(user=request.user.userprofile)  # Filter observations by current user

    
    return render(request, 'observationjournal.html', {'form': form, 'observations': observations, 'species': species})

def delete_observation(request, observation_id):
    if request.method == 'POST':  # If the form has been submitted
        observation = UserObservation.objects.get(pk=observation_id) # Get the observation object
        observation.delete() # Delete the observation object
        return HttpResponseRedirect(reverse('journal_view'))  # Redirect back to the journal view