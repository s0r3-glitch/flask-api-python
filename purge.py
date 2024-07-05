import pymongo
from pymongo.server_api import ServerApi

uri = "L+Ratio"
myclient = pymongo.MongoClient(uri, server_api=ServerApi('1'))
dblist = myclient.list_database_names()
for i in range(len(dblist)):
    print(i)
    myclient.drop_database(dblist[i])