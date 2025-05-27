from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://FastApi:abc%40123@aayush.0ykxxqv.mongodb.net/?retryWrites=true&w=majority&appName=aayush"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db
collection = db["todo_data"]