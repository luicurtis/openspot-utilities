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
parkingLot_db = db_name["parking_lot"]


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

            # check if the place mark is the panning limit
            if spotID == "Panning Limit":
                print("found panning limit")
                try:
                    limits = spot.Polygon.outerBoundaryIs.LinearRing.coordinates.text.split('\n')

                    # clean up parsed data
                    # remove first and last index since it is empty text
                    limits.pop(0)
                    limits.pop(5)
                    polygons = []

                    for i,coord in enumerate(limits):
                        splitCoord = coord.strip().split(',')
                        splitCoord.pop(2) # remove useless 0
                        polygons.append({
                            'lat': float(splitCoord[1]),    # second element is lat
                            'lng': float(splitCoord[0])     # first element is long
                        })

                    # extract most north, east, south, west coordinates
                    bounds = {
                        'north': polygons[0]['lat'],
                        'east': polygons[2]['lng'],
                        'south': polygons[2]['lat'],
                        'west': polygons[0]['lng'],
                    }

                    center = {
                        'lat': 	(bounds['north']+bounds['south']) / 2,
                        'lng': 	(bounds['east']+bounds['west']) / 2
                    }

                    print(bounds)                    
                    print(center)
                    parkingLotIdentifier = {'parkingLotName' : parkingLotName}

                    parkingLotRecord = {'parkingLotName' : parkingLotName,
                                        'bounds' : bounds,
                                        'center' : center,
                                        } 

                    parkingLot_db.update_one(parkingLotIdentifier, {"$set":parkingLotRecord}, upsert=True)
                    
                except:
                    # Encountered a pin that represents where the module is placed
                    print('this is a pin')
                    continue
            else:
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
                    print('this is a pin')
                    totalSpots -= 1
                    continue
            
        # insert module record into db
        if modID != "Panning Limit":
            moduleIdentifier = {'parkingLotName' : parkingLotName,
                                'modID': int(modID)}

            moduleRecord = {'parkingLotName' : parkingLotName,
                            'ledColour' : 0,
                            'numSpotsFull': 0,
                            'totalSpots' : totalSpots,
                            'modID': int(modID)
                            }
            module_db.update_one(moduleIdentifier, {"$set":moduleRecord}, upsert=True)
        