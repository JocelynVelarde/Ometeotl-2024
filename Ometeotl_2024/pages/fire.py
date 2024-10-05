"""The fire map page."""

from ..templates import template
from Ometeotl_2024.components.map import fire_map
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from ..backend.json_encoder import JSONEncoder

import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(uri=os.getenv("MONGO_URI"), server_api=ServerApi('1'))

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

@template(route="/fire", title="Fire")
def fire() -> rx.Component:
    """The fire map page.

    Returns:
        The UI for the fire map page.
    """
    return rx.vstack(
        rx.heading("Fire map", size="5"),
        fire_map(),
        spacing="8",
        width="100%",
    )
