from . import db
from typing import Dict
from src.modules.Serializer import Serializer
from datetime import datetime
from bson.objectid import ObjectId


admins = db.admins

class Admin:

    @staticmethod
    def create_admin(new_admin: Dict) -> bool:
        db_response = admins.insert_one({
            'name':new_admin['name'],
            'password':new_admin['password'],
            'email': new_admin['email'],
            'created_at': datetime.now(),
            'updated_at': None,
            'type': new_admin['type']
        })

        return True if db_response.inserted_id else False

    @staticmethod
    def get_admin_by_email(email:str,needed_attributes=['_id','email','password','name','type','created_at','updated_at']) -> Dict:
        db_response = admins.find_one({'email':email})
        return Serializer(needed_attributes).serialize(db_response) if db_response else {}

    @staticmethod
    def get_admin_by_type(type:str,needed_attributes=['_id','email','password','name','type','created_at','updated_at']) -> Dict:
        db_response = admins.find_one({'type': type})
        if db_response:
            return Serializer(needed_attributes).serialize(db_response)

        return {}

    @staticmethod
    def get_admin_by_id(id: str, needed_attributes=['_id', 'email', 'password', 'name', 'type', 'created_at', 'updated_at']) -> Dict:
        db_response = admins.find_one({'_id': ObjectId(id)})
        return Serializer(needed_attributes).serialize(db_response) if db_response else {}

    @staticmethod
    def update_admin_password(admin_id:str,password:str) -> bool:
        query = admins.update_one({'_id': ObjectId(admin_id)}, {'$set': {'password': password, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False
    
    @staticmethod
    def update_admin_email(admin_id:str,email:str) -> bool:
        query = admins.update_one({'_id': ObjectId(admin_id)}, {'$set': {'email': email, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False
    
    @staticmethod
    def update_admin_name(admin_id:str,name:str) -> bool:
        query = admins.update_one({'_id': ObjectId(admin_id)}, {'$set': {'name': name, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False
    
    @staticmethod
    def delete_admin(email: str) -> bool:
        db_response = admins.find_one_and_delete({'email': email})
        return True if db_response else False
