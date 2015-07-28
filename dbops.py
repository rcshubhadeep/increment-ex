from pymongo import MongoClient


def get_db_details(appconfig):
    try:
        client = MongoClient(appconfig["SERVER"], appconfig["PORT"])
        db = client[appconfig["DB_NAME"]]
        collection = db[appconfig["COLLECTION_NAME"]]
        return collection
    except Exception:
        return None


def inc_value(inc_key, app):
    collection = get_db_details(app.config)
    if collection == None:
        return {"value": -1}, 400
    row = collection.find_one({"key": inc_key})
    if not row:
        collection.insert_one({"key": inc_key, "val": 1})
        return {"value": 1}, 201
    else:
        collection.update({"key": inc_key}, {"$inc": {"val": 1}})
        # One fetch less but same effect.
        return {"value": row["val"] + 1}, 200


def set_val(inc_key, value, app):
    collection = get_db_details(app.config)
    if collection == None:
        return {"value": -1}, 404
    row = collection.find_one({"key": inc_key})
    if not row:
        collection.insert_one({"key": inc_key, "val": 1})
        return {"value": 1}, 201
    else:
        collection.update({"key": inc_key, }, {"$set": {"val": value}})
        return {"value": row["val"]}, 200
