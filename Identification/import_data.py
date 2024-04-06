from Identification.models import State, SnakeSpecies
from Identification.state_data import states

'''
This is a file with methods to import data into our DB from the django shell
To access the shell -> python manage.py shell
Then import whatever functions you wish to use from this file, and call the functions in shell
'''


# A function to add our states data to the database
def add_states():
    for name, abbreviation in states:
        State.objects.get_or_create(name=name, abbreviation=abbreviation)
    print("All states have been added.")

# A function to clear the states table in our DB
def clear_states():
    State.objects.all().delete()
    print("All states have been deleted.")

