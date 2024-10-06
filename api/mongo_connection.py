
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from json import JSONEncoder

import streamlit as st

client = MongoClient(uri=st.secrets['MONGO_URI'], server_api=ServerApi('1'))

def insert_data(data :str, database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        result = collection.insert_one(data)
        
        print(f'Data inserted successfully with id: {result.inserted_id}')
    except Exception as e:
        print("Error inserting data: ", e)

def get_one_data(query: str, database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        data = collection.find_one(query)
        
        return JSONEncoder().encode(data)
    
    except Exception as e:
        print("Error getting data: ", e)
        return {"error": f'Error getting data {e}'}
