from django import forms

from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

def login_view(request):
    """
    This view handles the login functionality.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered response with the 'login.html' template.
    """
    return render(request, 'login.html')

def register_view(request):
    """
    This view handles the registration process for new users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered 'register.html' template.
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST) # Create a form instance and populate it with data from the request
        profile_form = UserProfileForm(request.POST) # Create a form instance and populate it with data from the request
        if user_form.is_valid() and profile_form.is_valid(): # Check if the form is valid
            user = user_form.save() # Save the user form
            profile = profile_form.save(commit=False) # Save the profile form
            profile.user = user # Link the profile to the user
            profile.save() # Save the profile

            # Log the user in and redirect them to their profile page
            return redirect('profile')
    else:
        user_form = UserRegisterForm() # Create a blank form
        profile_form = UserProfileForm() # Create a blank form
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form}) # Render the registration form

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