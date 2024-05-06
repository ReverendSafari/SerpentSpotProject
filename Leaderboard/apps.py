from django.apps import AppConfig


class LeaderboardConfig(AppConfig):
    """
    AppConfig class for the Leaderboard app.

    This class represents the configuration for the Leaderboard app in a Django project.
    It sets the default auto field to 'django.db.models.BigAutoField' and specifies the name of the app as 'Leaderboard'.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Leaderboard'
