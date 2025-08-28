import pymongo
from connect_to_mongo.mongo_confing import HOST, DATABASE

def insert_to_mongo(collection,data):
    myclient = pymongo.MongoClient(HOST)
    mydb = myclient[DATABASE]
    mycol = mydb[collection]
    try:
        mycol.insert_many(data)
    except Exception as e:
        print(e)
    if mydb[collection].count_documents({}) > 0:
        massage = 'the insert topic has been updated'
    else:
        massage = 'the insert is not updated'
    print(massage)

insert_to_mongo('news',[{'news':1},{'news':2}])