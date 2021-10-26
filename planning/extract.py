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
            spotCoords = spot.Polygon.outerBoundaryIs.LinearRing.coordinates.text.split('\n')

            # clean up parsed data
            # remove first and last index since it is empty text
            spotCoords.pop(0)
            spotCoords.pop(5)

            parsedCoords = []
            for i,coord in enumerate(spotCoords):
                splitCoord = coord.strip().split(',')
                splitCoord.pop(2) # remove useless 0
                parsedCoords.append({
                    'lat': splitCoord[1],    # second element is lat
                    'lng': splitCoord[0]     # first element is long
                })
                # splittedCoord = strippedCoord.split(',')
                # print(str(i) + ': ' + strippedCoord)
                # print(type(splitCoord))
                # print(splitCoord)

            print(parsedCoords)
            # print(len(parsedCoords))