# @Vendors
import pymongo

# @Constants
from src.constants.constants import (DB_SERVER_URL, DB_CONNECTION_TIMEOUT)

def connect():
    return pymongo.MongoClient(DB_SERVER_URL, serverSelectionTimeoutMS=DB_CONNECTION_TIMEOUT)

def db_check_collection(db_name, col_name):
    db = connect()[db_name]
    try:
        return col_name in db.collection_names()
    except:
        raise ConnectionError()

def get_collection(db_name, col_name):
    db = connect()[db_name]
    return db[col_name]

def db_get_item(db_name, col_name, query=None, fields=None):
    try:
        col = get_collection(db_name, col_name)
        return col.find_one(query, fields)
    except:
        raise ConnectionError()

def db_get_items(db_name, col_name, query=None, fields=None):
    try:
        col = get_collection(db_name, col_name)
        return col.find(query, fields)
    except:
        raise ConnectionError()

def db_insert_item(db_name, col_name, element):
    try:
        col = get_collection(db_name, col_name)
        return col.insert_one(element)
    except:
        raise ConnectionError()

def db_insert_items(db_name, col_name, elements):
    try:
        col = get_collection(db_name, col_name)
        return col.insert(elements)
    except:
        raise ConnectionError()

def db_update_item(db_name, col_name, query, updated_items):
    try:
        col = get_collection(db_name, col_name)
        return col.update_one(query, { '$set': updated_items })
    except:
        raise ConnectionError()

def db_delete_item(db_name, col_name, query):
    try:
        col = get_collection(db_name, col_name)
        return col.delete_one(query)
    except:
        raise ConnectionError()

def db_drop_collection(db_name, col_name):
    try:
        col = get_collection(db_name, col_name)
        col.drop()
    except:
        raise ConnectionError()
