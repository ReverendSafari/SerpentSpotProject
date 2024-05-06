from django.apps import AppConfig


class ObservationjournalConfig(AppConfig):
    """
    AppConfig for the ObservationJournal app.

    This class represents the configuration for the ObservationJournal app in a Django project.
    It sets the default auto field to 'django.db.models.BigAutoField' and specifies the name of the app.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ObservationJournal'
