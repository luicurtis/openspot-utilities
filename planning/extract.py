from pykml import parser
from os import path
from pathlib import Path

PARENT_PATH = Path(__file__).parent
KML_PATH = PARENT_PATH / Path("./kml_files")

def relative_to_kml_files(path: str) -> Path:
    return KML_PATH / Path(path)

kml_file = path.join(relative_to_kml_files('kensington.kml'))

with open(kml_file) as f:
    doc = parser.parse(f).getroot()
    # print(dir(doc))
    parkingLotName = doc.Document.name.text
    print('Parking Lot Name: ' + parkingLotName)

    # loop through each module
    for module in doc.Document.Folder:
        modID = module.name.text
        print('modID: ' + modID)

        # loop through all spots of the module
        for spot in module.Placemark:
            spotID = spot.name.text
            print('spotID: ' + spotID)
            spotCoords = spot.Polygon.outerBoundaryIs.LinearRing.coordinates.text.split([',', '\n'])
            # spotCoords.split('\n')
            print(spotCoords)
            print(type(spotCoords))
            print(len(spotCoords))


        # for 
    # for e in doc.Document.Folder.Placemark:
        # print(e)
        # coor = e.Point.coordinates.text.split(',')
        # print(coor)
