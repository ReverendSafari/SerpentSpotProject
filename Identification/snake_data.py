"""
This is another utility file used in import_data.py
"""



"""
Parses a txt file (snaketext.txt) containing raw text data for snake species and cleans and stores it into dict's

Args:
    file_path: The file path to the txt file containing the snake data

Returns:
    list: A list of dictionaries containing the snake data
"""
def parse_snake_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding here
        lines = file.readlines()

    snakes_list = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue  # Skip incomplete lines

        common_name = parts[0]
        scientific_name = parts[1]
        venomous = True if parts[2].strip().upper() == "VENOMOUS" else False
        description = parts[3]
        states = parts[4].split(', ')

        # Format image path using common name
        image_path = f"img/{common_name.replace(' ', '').lower()}.jpg"

        # Create dictionary for each snake
        snake_dict = {
            'common_name': common_name,
            'scientific_name': scientific_name,
            'image_path': image_path,
            'description': description,
            'venomous': venomous,
            'states': states  # This will need to be handled appropriately in Django
        }

        snakes_list.append(snake_dict)

    return snakes_list

