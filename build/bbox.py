import yaml
from coordinates_generator import CoordinatesGenerator
from colors import *
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
YAML_PATH = OUTPUT_PATH / Path("./yaml_upload")


def relative_to_yaml(path: str) -> Path:
    return YAML_PATH / Path(path)

def DrawBBoxes(image_file, data_file=relative_to_yaml('coords.yml')):
    with open(data_file, "w+") as points:
        generator = CoordinatesGenerator(image_file, points, COLOR_RED)
        generator.generate()
    
    # upload 
    print('here')