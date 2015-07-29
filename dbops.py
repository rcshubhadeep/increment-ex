from pymongo import MongoClient
import os


def get_db_details(appconfig, applogger):
    if not appconfig["USING_DOCKER"]:
        try:
            client = MongoClient(appconfig["SERVER"], appconfig[
                                 "PORT"], serverSelectionTimeoutMS=1500)
            db = client[appconfig["DB_NAME"]]
            collection = db[appconfig["COLLECTION_NAME"]]
            return collection
        except Exception, ex:
            applogger("Error in connecting DB: ")
            return None
    else:
        try:
            client = MongoClient(os.environ[
                                 'INCREMENTEX_DB_1_PORT_27017_TCP_ADDR'], 27017,
                                  serverSelectionTimeoutMS=1500)
            db = client[appconfig["DB_NAME"]]
            collection = db[appconfig["COLLECTION_NAME"]]
            return collection
        except Exception, ex:
            applogger("Error in connecting DB via docker : ")
            return None


def inc_value(inc_key, app):
    collection = get_db_details(app.config, app.logger)  # Init the DB
    if collection == None:
        app.logger.error("Collection is None inc_value")
        return {"value": -1}, 400
    try:
        row = collection.find_one({"key": inc_key})  # try to find the record
        if not row:
            collection.insert_one({"key": inc_key, "val": 1})
            return {"value": 1}, 201
        else:
            # If found. Update. Use $inc
            collection.update({"key": inc_key}, {"$inc": {"val": 1}})
            # One fetch less but same effect.
            return {"value": row["val"] + 1}, 200
    except Exception, ex:
        app.logger("Error in DB connection inc_value: ")
        return {"value": -1}, 404


def set_val(inc_key, value, app):
    collection = get_db_details(app.config, app.logger)  # Init the DB
    if collection == None:
        app.logger.error("Collection is None set_val")
        return {"value": -1}, 404
    try:
        row = collection.find_one({"key": inc_key})  # Try to find the record
        if not row:
            collection.insert_one({"key": inc_key, "val": 1})
            return {"value": 1}, 201
        else:
            # If record found. Update
            collection.update({"key": inc_key, }, {"$set": {"val": value}})
            return {"value": value}, 200
    except Exception, ex:
        app.logger("Error in DB connection inc_value: ")
        return {"value": -1}, 404
