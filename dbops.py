from pymongo import MongoClient


def get_db_details(appconfig, applogger):
    try:
        client = MongoClient(appconfig["SERVER"], appconfig[
                             "PORT"], serverSelectionTimeoutMS=1500)
        db = client[appconfig["DB_NAME"]]
        collection = db[appconfig["COLLECTION_NAME"]]
        return collection
    except Exception, ex:
        applogger("Error in connecting DB: ", ex)
        return None


def inc_value(inc_key, app):
    collection = get_db_details(app.config, app.logger)
    if collection == None:
        app.logger.error("Collection is None inc_value")
        return {"value": -1}, 400
    try:
        row = collection.find_one({"key": inc_key})
        if not row:
            collection.insert_one({"key": inc_key, "val": 1})
            return {"value": 1}, 201
        else:
            collection.update({"key": inc_key}, {"$inc": {"val": 1}})
            # One fetch less but same effect.
            return {"value": row["val"] + 1}, 200
    except Exception, ex:
        app.logger("Error in DB connection inc_value: ")
        return {"value": -1}, 404


def set_val(inc_key, value, app):
    collection = get_db_details(app.config, app.logger)
    if collection == None:
        app.logger.error("Collection is None set_val")
        return {"value": -1}, 404
    try:
        row = collection.find_one({"key": inc_key})
        if not row:
            collection.insert_one({"key": inc_key, "val": 1})
            return {"value": 1}, 201
        else:
            collection.update({"key": inc_key, }, {"$set": {"val": value}})
            return {"value": value}, 200
    except Exception, ex:
        app.logger("Error in DB connection inc_value: ")
        return {"value": -1}, 404
