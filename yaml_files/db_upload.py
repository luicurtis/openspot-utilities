import pymongo 

def connect_to_db():  
    my_client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.56jzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db_name = my_client["Backend"]
    collection_name = db_name["spots"]
    count = collection_name.count_documents({})
    print(count)

connect_to_db()