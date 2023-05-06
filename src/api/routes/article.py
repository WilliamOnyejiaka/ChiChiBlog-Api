from flask import Blueprint, jsonify, request
from typing import Dict, List
from src.api.models.Article import Article
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.valid_object_id import valid_object_id
from src.modules.response import response
from src.modules.Pagination import Pagination

article = Blueprint("article", __name__, url_prefix="/api/article")


@article.post("/create-article")
@jwt_required()
def create_article():
    identity = get_jwt_identity()

    if not valid_object_id(identity):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    title = request.get_json().get('title', None)
    body = request.get_json().get('body', None)
    image_url = request.get_json().get('image_url', None)

    if not title or not body:
        return jsonify({
            'error': True,
            'message': "title and body required"
        }), 400

    if len(title) < 3:
        return jsonify({
            'error': True,
            'message': "title length must be greater than 2"
        }), 400

    if len(body) < 3:
        return jsonify({
            'error': True,
            'message': "body length must be greater than 2"
        }), 400

    if Article.get_article_by_title(title):
        return jsonify({
            'error': True,
            'message': "an article with this title already exists"
        }), 400

    if Article.create_article({
        'title': title,
        'body': body,
        'image_url': image_url,
        'admin_id': identity
    }):
        return jsonify({
            'error': False,
            'message': "article created successfully"
        }), 201

    return jsonify({
        'error': True,
        'message': "something went wrong"
    }), 500


@article.get("/get-article/<id>")
@jwt_required()
def get_admin_article(id: str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    data: Dict = Article.get_admin_article(id, admin_id)

    if data:
        return jsonify({
            'error': False,
            'data': data
        }), 200

    return jsonify({
        'error': True,
        'message': "article not found"
    }), 404


@article.get("/get-all-articles")
@jwt_required()
def get_article():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    data: List = Article.get_admin_articles(admin_id)

    return jsonify({'error': False, 'data': data}), 200


@article.get("/pagination/article-pagination")
@jwt_required()
def article_pagination():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 1))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit must be an integer"}), 400

    paginate = Pagination(Article.get_admin_articles(
        admin_id), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200


@article.get("/search")
@jwt_required()
def article_search():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.admin_article_search(admin_id, search_string)
    return jsonify({'error': False, 'data': data}), 200


@article.get("/search/title")
@jwt_required()
def title_search():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.admin_title_search(admin_id, search_string)
    return jsonify({'error': False, 'data': data}), 200


@article.get("/search/body")
@jwt_required()
def body_search():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.admin_body_search(admin_id, search_string)
    return jsonify({'error': False, 'data': data}), 200


@article.get("/pagination/article-search")
@jwt_required()
def article_search_pagination():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    search_string = request.args.get('search-string', None)
    search_target = request.args.get('search-target', None)
    acceptable_targets = ['article', 'title', 'body']

    if not search_string or not search_target:
        return jsonify({'error': True, 'message': "all values needed"}), 400

    if search_target not in acceptable_targets:
        return jsonify({'error': True, 'message': "unacceptable search target"}), 400

    page = request.args.get('page', 1)
    limit = request.args.get('limit', 10)
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit must be an integer"}), 400

    paginate = []
    if search_target == "body":
        paginate = Pagination(Article.admin_body_search(
            admin_id, search_string), page, limit).meta_data()
    elif search_target == "title":
        paginate = Pagination(Article.admin_title_search(
            admin_id, search_string), page, limit).meta_data()
    else:
        paginate = Pagination(Article.admin_article_search(
            admin_id, search_string), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200


@article.patch("/update/update-body/<id>")
@jwt_required()
def update_body(id: str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    body: str = request.get_json().get('body', None)

    if not body:
        return jsonify({
            'error': True,
            'message': "body required"
        }), 400

    if len(body) < 3:
        return jsonify({
            'error': True,
            'message': "body length must be greater than 2"
        }), 400

    if Article.admin_update_body(id, admin_id, body):
        return jsonify({'error': False, 'message': "article body has been updated"}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@article.patch("/update/update-title/<id>")
@jwt_required()
def update_title(id: str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    title: str = request.get_json().get('title', None)

    if not title:
        return jsonify({
            'error': True,
            'message': "title required"
        }), 400

    if len(title) < 3:
        return jsonify({
            'error': True,
            'message': "title length must be greater than 2"
        }), 400

    if Article.get_article_by_title(title):
        return jsonify({
            'error': True,
            'message': "an article with this title already exists"
        }), 400

    if Article.admin_update_title(id, admin_id, title):
        return jsonify({'error': False, 'message': "article title has been updated"}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@article.patch("/update/update-image-url/<id>")
@jwt_required()
def update_image(id: str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    image_url: str = request.get_json().get('image_url', None)

    if not image_url:
        return jsonify({
            'error': True,
            'message': "image_url required"
        }), 400

    if Article.admin_update_image_url(id, admin_id, image_url):
        return jsonify({'error': False, 'message': "article image url has been updated"}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@article.put("/update/update-article/<id>")
@jwt_required()
def update_article(id: str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    image_url: str = request.get_json().get('image_url', None)
    title: str = request.get_json().get('title', None)
    body: str = request.get_json().get('body', None)

    if not image_url or not body or not title:
        return jsonify({
            'error': True,
            'message': "all values required"
        }), 400

    if len(title) < 3:
        return jsonify({
            'error': True,
            'message': "title length must be greater than 2"
        }), 400

    if Article.get_article_by_title(title):
        return jsonify({
            'error': True,
            'message': "an article with this title already exists"
        }), 400

    if len(body) < 3:
        return jsonify({
            'error': True,
            'message': "body length must be greater than 2"
        }), 400

    if Article.admin_update_article(id, admin_id, title, body, image_url):
        return jsonify({'error': False, 'message': "article image url has been updated"}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@article.delete("/delete/delete-image-url/<id>")
@jwt_required()
def delete_image_url(id:str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401
    
    if Article.get_article_by_id(id, admin_id):
        if Article.admin_delete_image_url(id, admin_id):
            return jsonify({'error': False, 'message': "image url has been deleted"}), 200
        return jsonify({'error': True, 'message': "something went wrong"}), 500
    return jsonify({'error': True, 'message': "article not found"}), 404

@article.delete("/delete/<id>")
@jwt_required()
def delete_article(id:str):
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401
    
    if Article.get_article_by_id(id, admin_id):
        if Article.admin_delete_article(id, admin_id):
            return jsonify({'error': False, 'message': "article has been deleted"}), 200
        return jsonify({'error': True, 'message': "something went wrong"}), 500
    return jsonify({'error': True, 'message': "article not found"}), 404
