from pykml import parser
from os import path
from pathlib import Path

import pymongo 
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Upload Parking Lot Spot information to .kml file to database')

    parser.add_argument("-kml",
                        dest="kml_file",
                        required=True,
                        help="kml map file to extract coordinates and upload to database")
    return parser.parse_args()

args = parse_args()
kml_file = args.kml_file

MongoDBclient = pymongo.MongoClient("mongodb+srv://root:root@cluster0.56jzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db_name = MongoDBclient["Backend"]
spots_db = db_name["spots"]
module_db = db_name["module"]

with open(kml_file) as f:
    doc = parser.parse(f).getroot()
    parkingLotName = doc.Document.name.text

    # loop through each module
    for module in doc.Document.Folder:
        modID = module.name.text

        totalSpots = 0
        # loop through all spots of the module
        for spot in module.Placemark:
            totalSpots += 1
            spotID = spot.name.text

            try:
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

            except:
                # Encountered a pin that represents where the module is placed
                # print('this is a pin')
                continue
            
        # insert module record into db
        moduleIdentifier = {'parkingLotName' : parkingLotName,
                            'modID': int(modID)}

        moduleRecord = {'parkingLotName' : parkingLotName,
                        'ledColour' : 0,
                        'numSpotsFull': 0,
                        'totalSpots' : totalSpots,
                        'modID': int(modID)}

        module_db.update_one(moduleIdentifier, {"$set":moduleRecord}, upsert=True)