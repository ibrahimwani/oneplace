from app import test_registration, test_login

test_registration()
test_login()
# from pymongo import MongoClient

# # MongoDB connection URI for localhost
# client = MongoClient("mongodb://127.0.0.1:27017/")  # Using the default port 27017

# # Access the database (create a new one if it doesn't exist)
# db = client["mydatabase"]  # Replace "mydatabase" with your desired database name

# # Print the database name to confirm connection
# print("Connected to database:", db.name)

# # Test connection by listing available collections in the database
# print("Collections in the database:", db.list_collection_names())
