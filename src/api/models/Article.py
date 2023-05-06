from . import db
from typing import Dict,List
from src.modules.Serializer import Serializer
from datetime import datetime
from bson.objectid import ObjectId

articles = db.articles


class Article:

    @staticmethod
    def create_article(new_article:Dict) -> bool:
        db_response = articles.insert_one({
            'title': new_article['title'],
            'body': new_article['body'],
            'image_url': new_article['image_url'],
            'admin_id': new_article['admin_id'],
            'created_at': datetime.now(),
            'updated_at': None,
        })

        return True if db_response.inserted_id else False
    
    @staticmethod
    def get_article(query_values:Dict,needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> Dict:
        db_response = articles.find_one(query_values)
        return Serializer(needed_attributes).serialize(db_response) if db_response else {}
    
    @staticmethod
    def get_article_by_id(id: str,admin_id:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> Dict:
        return Article.get_article({'_id': ObjectId(id), 'admin_id': admin_id}, needed_attributes)
        
    @staticmethod
    def get_article_by_title(title: str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> Dict:
        return Article.get_article({'title': title}, needed_attributes)

    @staticmethod
    def get_admin_article(id:str, admin_id:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> Dict:
        return Article.get_article({'_id': ObjectId(id), 'admin_id': admin_id},needed_attributes)
    
    @staticmethod
    def get_admin_articles(admin_id:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> List:
        db_response:List = list(articles.find({'admin_id': admin_id}).sort('_id'))
        return Serializer(needed_attributes).dump(db_response) if db_response else []

    @staticmethod
    def admin_article_search(admin_id:str, search_string:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> List:
        db_response = list(articles.find({'admin_id': admin_id, '$or': [{
            'body': {
                '$regex': search_string,
                "$options": 'i'
            }},
            {
            'title': {
                '$regex': search_string,
                "$options": 'i'
            }}
        ]}).sort('_id'))

        return Serializer(needed_attributes).dump(db_response)
    
    @staticmethod
    def admin_title_search(admin_id:str, search_string:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> List:
        db_response = list(articles.find({'admin_id': admin_id,'title': {'$regex': search_string,"$options": 'i'}}).sort('_id'))
        return Serializer(needed_attributes).dump(db_response)

    @staticmethod
    def admin_body_search(admin_id:str, search_string:str, needed_attributes=['_id', 'title', 'body', 'image_url', 'created_at', 'updated_at']) -> List:
        db_response = list(articles.find({'admin_id': admin_id,'body': {'$regex': search_string,"$options": 'i'}}).sort('_id'))
        return Serializer(needed_attributes).dump(db_response)
    
    @staticmethod
    def update_article(id:str,admin_id:str,query_values:Dict) -> bool:
        query_values['updated_at'] = datetime.now()
        db_response = articles.update_one(
            {'_id': ObjectId(id), 'admin_id': admin_id}, {'$set': query_values})
        return True if db_response.raw_result['nModified'] == 1 else False
    
    @staticmethod
    def admin_update_body(id:str, admin_id:str,body:str) -> bool:
        return Article.update_article(id,admin_id,{'body':body})

    @staticmethod
    def admin_update_title(id: str, admin_id: str, title: str) -> bool:
        return Article.update_article(id, admin_id, {'title': title})

    @staticmethod
    def admin_update_article(id:str, admin_id:str,title:str,body:str,image_url:str) -> bool:
        return Article.update_article(id, admin_id, {'body': body, 'title': title, 'image_url': image_url})

    @staticmethod
    def admin_update_image_url(id: str, admin_id: str, image_url: str) -> bool:
        return Article.update_article(id, admin_id, {'image_url': image_url})
    
    @staticmethod
    def admin_delete_image_url(id: str, admin_id: str):
        return Article.update_article(id, admin_id, {'image_url': None})
    
    @staticmethod
    def admin_delete_article(id: str, admin_id: str):
        db_response = articles.find_one_and_delete({'_id': ObjectId(id),'admin_id':admin_id})
        return True if db_response else False   

