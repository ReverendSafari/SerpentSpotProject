from django import forms # Import the forms module from Django
from django.contrib.auth.forms import UserCreationForm # Import the UserCreationForm from Django
from django.contrib.auth.models import User # Import the User model from Django

from .models import UserProfile # Import the UserProfile model from the current app

# Seamus 
class UserRegisterForm(UserCreationForm):
    """
    A form used for user registration.

    Inherits from UserCreationForm, which is a built-in form provided by Django for user registration.
    Adds an email field to the form.

    Attributes:
        email (forms.EmailField): The email field for the user's email address.

    Meta:
        model (User): The User model that the form is associated with.
        fields (list): The fields that will be displayed in the form.
    """
    email = forms.EmailField()

    class Meta:
        model = User # The User model that the form is associated with
        fields = ['username', 'email', 'password1', 'password2'] # The fields that will be displayed in the form

# Seamus 
class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profile information.

    This form is used to display and update the user's bio, profile picture, and favorite species.

    Attributes:
        bio (CharField): A field for the user's bio.
        profile_pic (ImageField): A field for the user's profile picture.
        favorite_species (CharField): A field for the user's favorite species.

    """
    class Meta:
        model = UserProfile # The UserProfile model that the form is associated with
        fields = ['bio', 'profile_pic', 'favorite_species'] # The fields that will be displayed in the form