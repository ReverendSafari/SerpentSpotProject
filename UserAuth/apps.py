from django.apps import AppConfig

class AuthConfig(AppConfig):
    """
    AppConfig class for the UserAuth app.

    This class represents the configuration for the UserAuth app in the Django project.
    It specifies the default auto field and the name of the app.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField' # This is the default auto field
    name = 'UserAuth' # This is the name of the app
