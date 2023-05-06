from pymongo import MongoClient
from src.config import MONGODB_URI

mongo = MongoClient(MONGODB_URI)
db = mongo.chichi_blog_db
