import pymongo
from pymongo.server_api import ServerApi
import datetime
uri = "L+Ratio"
myclient = pymongo.MongoClient(uri, server_api=ServerApi('1'))

try:
    myclient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    exit(88)

#gets a lis of all the databases
dbs = myclient.list_database_names()

#iterate over the list of databases
for db in dbs:
    #get the database
    mydb = myclient[db]
    #get a list of all the collections
    collist = mydb.list_collection_names()
    if "keepalive" in collist:
        #get the collection
        mycol = mydb["keepalive"]
        #get the document matching ka: ka
        myquery = { "ka": "ka" }
        mydoc = mycol.find(myquery)
        #get the data in LastBeat
        for x in mydoc:
            print(x['LastBeat'])
            #get the current time
            now = datetime.datetime.now()
            #get the time difference
            diff = now - x['LastBeat']
            #if the difference is greater than 10 seconds
            if diff.seconds > 6000:
                print("Deleting the document")
                mycol.delete_one(myquery)

