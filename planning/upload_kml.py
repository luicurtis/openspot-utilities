from pykml import parser
from os import path
from pathlib import Path

import pymongo 

PARENT_PATH = Path(__file__).parent
KML_PATH = PARENT_PATH / Path("./kml_files")

def relative_to_kml_files(path: str) -> Path:
    return KML_PATH / Path(path)

MongoDBclient = pymongo.MongoClient("mongodb+srv://root:root@cluster0.56jzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = MongoDBclient["Backend"]
spots_db = db_name["spots"]
module_db = db_name["module"]

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

        totalSpots = 0
        # loop through all spots of the module
        for spot in module.Placemark:
            totalSpots += 1
            spotID = spot.name.text
            print('spotID: ' + spotID)
            spotCoords = spot.Polygon.outerBoundaryIs.LinearRing.coordinates.text.split('\n')

            # clean up parsed data
            # remove first and last index since it is empty text
            spotCoords.pop(0)
            spotCoords.pop(5)

            polygons = []
            for i,coord in enumerate(spotCoords):
                splitCoord = coord.strip().split(',')
                splitCoord.pop(2) # remove useless 0
                polygons.append({
                    'lat': float(splitCoord[1]),    # second element is lat
                    'lng': float(splitCoord[0])     # first element is long
                })
                # splittedCoord = strippedCoord.split(',')
                # print(str(i) + ': ' + strippedCoord)
                # print(type(splitCoord))
                # print(splitCoord)

            print(polygons)
            # print(len(parsedCoords))
            
            # insert spot record into db
            spotIdentifier = {  'parkingLotName' : parkingLotName,
                                'modID': int(modID),
                                'spotNum': int(spotID)}

            spotRecord = {  'parkingLotName' : parkingLotName,
                            'modID': int(modID),
                            'spotNum': int(spotID),
                            'occupied': False,
                            'polygons': polygons
                            }
            
            spots_db.update_one(spotIdentifier, {"$set":spotRecord}, upsert=True)

        # insert module record into db
        print(totalSpots)
        moduleIdentifier = {'parkingLotName' : parkingLotName,
                            'modID': int(modID)}

        moduleRecord = {'parkingLotName' : parkingLotName,
                        'ledColour' : 0,
                        'numSpotsFull': 0,
                        'totalSpots' : totalSpots,
                        'modID': int(modID)}

        module_db.update_one(moduleIdentifier, {"$set":moduleRecord}, upsert=True)