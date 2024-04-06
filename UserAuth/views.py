from django import forms

from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import UserProfile

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
                messages.info(request, f"You are now logged in as {username}.")
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

class UserRegisterForm(UserCreationForm):
    """
    A form for registering a new user.

    Inherits from UserCreationForm and adds an email field.

    Attributes:
        email (forms.EmailField): The email field for the user's email address.

    Meta:
        model (User): The User model to be used for registration.
        fields (list): The fields to be included in the form.

    """
    email = forms.EmailField()

    class Meta:
        model = User # Link the form to the User model
        fields = ['username', 'email', 'password1', 'password2'] # Include the specified fields in the form

class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profile information.

    This form is used to update the user's profile information, specifically the 'bio' field.

    Attributes:
        model (UserProfile): The model associated with the form.
        fields (list): The fields to include in the form.

    """
    class Meta:
        model = UserProfile # Link the form to the UserProfile model
        fields = ['bio'] # Include the 'bio' field in the form