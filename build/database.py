# Class to perform database actions
import pymongo 
import yaml

class database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.56jzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db_name = self.client["Backend"]
        self.bbox_db = self.db_name["bbox_ref"]
        self.spots_db = self.db_name["spots"]
        self.module_db = self.db_name["module"]
        self.parkinglotInfo = {}

        for parking_lot_names in self.module_db.find():
            parking_lot_name = parking_lot_names["parkingLotName"]
            self.parkinglotInfo.setdefault(parking_lot_name, [])
            self.parkinglotInfo[parking_lot_name].append(parking_lot_names["modID"])

    # TODO: Call DB functions (DONE)
    # - get all parking lot names
    # - get list of mod ids that exist
    # { "SFU" : [1,2,4,423,3]}

    #get list of parking lot names that exist
    def get_parking_lot_names(self):
        return(self.parkinglotInfo.keys())

    #get list of modIDs based on parking lot name
    #parking_lot_name = parking lot name that you want modIDs for
    def get_mod_ids(self, parking_lot_name):
        return(self.parkinglotInfo[parking_lot_name])

    #insert bounding box spots
    #yaml_file_path = path to yaml file
    #parking_lot_name = parking lot name 
    #modID = modID of the newly installed module
    def upload_bounding_boxes(self, yaml_file_path, parking_lot_name, modID, exist=False):
        # ref_yaml_file = open("./yaml_files/" + file_name)
        ref_yaml_file = open(yaml_file_path)
        parsed_ref = yaml.load(ref_yaml_file, Loader=yaml.FullLoader)

        refSpots = []
        #upload the coordinates used by the computer vision
        for spotnum, bbox in enumerate(parsed_ref):
            coord = bbox["coordinates"]
            # coordiantes are in (x,y)
            newSpot = ([coord[0][0], coord[0][1]],  # top left 
                        [coord[1][0], coord[1][1]], # top right
                        [coord[2][0], coord[2][1]], # bottom right
                        [coord[3][0], coord[3][1]]) # bottom left
            refSpots.append(newSpot)

        dict_insert = {"parkingLotName" : parking_lot_name,
                        "modID" : modID,
                        "mapping" : refSpots}
        
        self.bbox_db.update_one({"parkingLotName" : parking_lot_name, "modID" : modID},
                                {"$set":dict_insert}, 
                                upsert=True)       
    

# #how to use the class, examples.
# new_db = database()
# modID = new_db.get_mod_ids("Kensington")
# print(modID)
# parking_lot_names = list(new_db.get_parking_lot_names())
# print(parking_lot_names)
