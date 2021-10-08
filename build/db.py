# Class to perform database actions
import pymongo 

class database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.56jzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db_name = client["Backend"]
        self.bbox_db = db_name["bbox_ref"]
        self.spots_db = db_name["spots"]
        self.parkinglotInfo = {}
        # TODO: build dict of parking lot info
        # { "SFU" : [1,2,4,423,3]}

    # TODO: Call DB functions
    # - get all parking lot names
    # - get list of mod ids that exist
    # { "SFU" : [1,2,4,423,3]}

