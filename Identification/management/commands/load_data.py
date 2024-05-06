from django.core.management.base import BaseCommand, CommandError
from Identification.models import State, SnakeSpecies
from Identification.state_data import states
from Identification.snake_data import parse_snake_data

class Command(BaseCommand):
    help = 'Loads snake species and states data into the database'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clears all existing data before loading new data')

    def handle(self, *args, **options):
        file_path = 'Identification/snaketext.txt'  # Ensure correct path formatting
        if options['clear']:
            self.clear_states()
            self.clear_species()

        snakes_data = parse_snake_data(file_path)  # Call within command to avoid top-level execution issues
        self.add_states()
        self.load_snakes_to_db(snakes_data)
        self.stdout.write(self.style.SUCCESS('All data has been successfully imported.'))

    def add_states(self):
        for name, abbreviation in states:
            abbreviation = abbreviation.upper()
            State.objects.get_or_create(name=name, abbreviation=abbreviation)
        self.stdout.write(self.style.SUCCESS("All states have been added."))

    def clear_states(self):
        State.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All states have been deleted."))

    def clear_species(self):
        SnakeSpecies.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All species have been deleted."))

    def load_snakes_to_db(self, snakes_data):
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
               state_abbr = state_abbr.upper()  # Ensure abbreviation is uppercase
            try:
                state_obj = State.objects.get(abbreviation=state_abbr)
                snake_obj.states.add(state_obj)
            except State.DoesNotExist:
                print(f"State with abbreviation {state_abbr} does not exist.")
            snake_obj.save()
