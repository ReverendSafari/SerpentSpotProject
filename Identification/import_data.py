from Identification.models import State, SnakeSpecies
from Identification.state_data import states
from Identification.snake_data import parse_snake_data

'''
This is a file with methods to import data into our DB from the django shell
To access the shell -> python manage.py shell
Then import whatever functions you wish to use from this file, and call the functions in shell
'''
#Necessary variables to get the snake data
file_path = 'Identification\snaketext.txt'
snakes_data = parse_snake_data(file_path)



# A function to add our states data to the database
def add_states():
    for name, abbreviation in states:
        State.objects.get_or_create(name=name, abbreviation=abbreviation)
    print("All states have been added.")

# A function to clear the states table in our DB
def clear_states():
    State.objects.all().delete()
    print("All states have been deleted.")

# A function to clear our SnakeSpecies table in our DB
def clear_species():
    SnakeSpecies.objects.all().delete()
    print("All species have been deleted.")

# A function to add our snake species data to the database
def load_snakes_to_db(snakes_data):
    for snake in snakes_data:
        snake_obj, created = SnakeSpecies.objects.update_or_create(
            common_name=snake['common_name'],
            defaults={
                'scientific_name': snake['scientific_name'],
                'image_path': snake['image_path'],
                'description': snake['description'],
                'venomous': snake['venomous'],
            }
        )
        for state_abbr in snake['states']:
            state_obj, created = State.objects.get_or_create(
                abbreviation=state_abbr,
                defaults={'name': state_abbr}  
            )
            snake_obj.states.add(state_obj)
        snake_obj.save()
