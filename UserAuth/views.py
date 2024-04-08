from django import forms

from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import UserProfile

from.forms import UserProfileForm, UserRegisterForm

def login_view(request):
    """
    This view handles the login functionality.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered response with the 'login.html' template.
    """
    user = request.user

    if user.is_authenticated: # If the user is already logged in
        return redirect('profile') # Redirect to the profile page 
    
    if request.method == 'POST': # If the form has been submitted
        form = AuthenticationForm(request, data=request.POST) # Create a form instance
        if form.is_valid(): # Check if the form is valid
            username = form.cleaned_data.get('username') # Get the username from the form
            password = form.cleaned_data.get('password') # Get the password from the form
            user = authenticate(username=username, password=password) # Authenticate the user
            if user is not None: # If the user is authenticated
                login(request, user)
                messages.info(request, f"You were last logged in as {username}.")
                return redirect('profile') # Redirect to the profile page
            else:
                messages.error(request,"Invalid username or password.")  # If the user is not authenticated, display an error message
        else:
            messages.error(request,"Invalid username or password.") 
    else: # If the form has not been submitted
        form = AuthenticationForm() # Create an empty form
    return render(request, 'login.html', {'form': form}) # Render the login page with the form

def register_view(request):
    """
    This view handles the registration process for new users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered 'register.html' template.
    """
    if request.method == 'POST': # If the form has been submitted
        user_form = UserRegisterForm(request.POST) # Create a user form instance
        profile_form = UserProfileForm(request.POST) # Create a profile form instance
        if user_form.is_valid() and profile_form.is_valid(): # Check if both forms are valid
            with transaction.atomic(): # Use a transaction to ensure data consistency
                user = user_form.save() # Save the user form data
                profile, created = UserProfile.objects.get_or_create(user=user) # Get or create a user profile

                if created: # If the profile was newly created, populate it with form data
                    profile_form = UserProfileForm(request.POST, instance=profile)
                    if profile_form.is_valid():
                        profile_form.save()
            # Redirect to user's profile page
            login(request, user)  # Log the user in
            return redirect('profile')
        
    else: # If the form has not been submitted
        user_form = UserRegisterForm() # Create an empty user form
        profile_form = UserProfileForm() # Create an empty profile form
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form}) # Render the registration page with the forms

@login_required
def profile_view(request):
    """
    View function for displaying user profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered 'profile.html' template.
    """
    return render(request, 'profile.html')

@login_required
def edit_profile_view(request):
    """
    View function for editing user profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered 'editprofile.html' template.
    """
    if request.method == 'POST':
        # Assuming you have a form class `UserProfileForm` for handling the profile data
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page or wherever appropriate

    else:
        # Display the form with the current profile data
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'editprofile.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect response to the login page.
    """
    logout(request)
    return redirect('login')