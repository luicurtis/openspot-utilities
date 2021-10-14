import yaml
from coordinates_generator import CoordinatesGenerator
from colors import *

def DrawBBoxes(image_file, data_file='yaml_upload/coords.yml'):
    with open(data_file, "w+") as points:
        generator = CoordinatesGenerator(image_file, points, COLOR_RED)
        generator.generate()
    
    # upload 
    print('here')