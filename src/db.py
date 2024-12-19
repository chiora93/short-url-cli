import pymongo

import settings

database_client = pymongo.MongoClient(settings.DATABASE_URL)
database = database_client[settings.DATABASE_NAME]