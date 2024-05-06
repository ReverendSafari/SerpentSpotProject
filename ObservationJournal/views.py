from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.models import User

from Identification.models import SnakeSpecies, State

from .models import UserObservation
from .forms import ObservationForm

def journal_view(request, username=None):
    """
    View function for the observation journal page.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str, optional): The username in the URL. Defaults to None.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the user object based on the username is not found.

    """
    
    # Get the user object based on the username in the URL
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    species = SnakeSpecies.objects.all()  # Get all snake species
    if request.method == 'POST':
        form = ObservationForm(request.POST, request.FILES) # Create a form instance with POST data
        if form.is_valid(): # Check if the form data is valid
            observation = form.save(commit=False) # Create, but don't save the new observation object
            observation.species = form.cleaned_data['species'] # Set the species of the observation
            observation.latitude = form.cleaned_data.get('latitude')  # Capture latitude
            observation.longitude = form.cleaned_data.get('longitude')  # Capture longitude
            observation.user = request.user.userprofile  # Link the observation to the current user
            observation.save() # Save the observation object
            observation.user.observations += 1  # Increment observation count 
            observation.user.save()
            return redirect('journal_view')  # Redirect to avoid re-posting
        
    else: # If the form has not been submitted
        form = ObservationForm() # Create an empty form

    observations = UserObservation.objects.all()  # Get all observations
    observations = observations.filter(user=user.userprofile)  # Filter observations by current user

    
    return render(request, 'observationjournal.html', {'form': form, 'observations': observations, 'species': species, 'user': user})

def delete_observation(request, observation_id):
    """
    Deletes an observation from the database.

    Args:
        request (HttpRequest): The HTTP request object.
        observation_id (int): The ID of the observation to be deleted.

    Returns:
        HttpResponseRedirect: A redirect response to the journal view.
    """

    if request.method == 'POST':  # If the form has been submitted
        observation = UserObservation.objects.get(pk=observation_id) # Get the observation object
        observation.delete() # Delete the observation object
        return HttpResponseRedirect(reverse('journal_view'))  # Redirect back to the journal view