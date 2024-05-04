from django.shortcuts import render 
from django.db.models import Count
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from UserAuth.models import UserProfile
from ObservationJournal.models import UserObservation

@login_required
def leaderboard_view(request):
    """
    Renders the leaderboard view with information about the top 10 users and the current user's ranking.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered leaderboard view.

    """
    today = now() # Get the current date and time
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # Get the first day of the current month

    # Retrieve the current month's observations, grouped by user and counted
    month_observations = UserObservation.objects.filter( 
        date__gte=start_of_month, 
        date__lt=today
    ).values('user').annotate(observation_count=Count('id')).order_by('-observation_count')

    # Retrieve the top 10 user profiles for the leaderboard
    top_ten_profiles = UserProfile.objects.filter(
        id__in=[obs['user'] for obs in month_observations[:10]]
    ).annotate(
        observations_count=Count('userobservation')
    ).order_by('-observations_count')

    # Find the current user's profile
    current_user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    current_user_observations_this_month = UserObservation.objects.filter(
        user=current_user_profile, 
        date__gte=start_of_month,
        date__lt=today
    ).count()

    # Check if the current user is in the top 10
    is_user_ranked = current_user_profile in top_ten_profiles

    # If there are fewer than 10 users, everyone is ranked
    if len(month_observations) < 10:
        is_user_ranked = True

    # Find the number of observations needed to reach the 10th place
    observations_to_join = 0
    if not is_user_ranked and month_observations: # If the user is not ranked and there are observations
        tenth_place_count = month_observations[9]['observation_count'] if len(month_observations) >= 10 else 0 # Get the 10th place observation count
        observations_to_join = tenth_place_count - current_user_observations_this_month + 1 # Calculate the number of observations needed to join the top 10

    context = { # Define the context dictionary
        'top_ten_profiles': top_ten_profiles, # Add the top 10 profiles to the context
        'current_user_profile': current_user_profile, # Add the current user's profile to the context
        'current_user_observations_this_month': current_user_observations_this_month, # Add the current user's observations this month to the context
        'is_user_ranked': is_user_ranked, # Add the user's ranking status to the context
        'observations_to_join': observations_to_join, # Add the number of observations needed to join the top 10 to the context
    }

    return render(request, 'leaderboard.html', context)
