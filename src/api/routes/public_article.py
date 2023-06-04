from flask import Blueprint, jsonify, request
from typing import Dict, List
from src.api.models.Article import Article
from src.modules.valid_object_id import valid_object_id
from src.modules.Pagination import Pagination
from flask_jwt_extended import jwt_required

public_article = Blueprint("public_article", __name__, url_prefix="/api/public-article")

@public_article.get("/get-article/<id>")
def get_article(id: str):

    data: Dict = Article.get_public_article_by_id(id)

    if data:
        return jsonify({
            'error': False,
            'data': data
        }), 200

    return jsonify({
        'error': True,
        'message': "article not found"
    }), 404


@public_article.get("/get-all-articles")
def get_all_article():
    data: List = Article.get_all_articles()
    return jsonify({'error': False, 'data': data}), 200


@public_article.get("/pagination/article-pagination")
def article_pagination():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit must be an integer"}), 400

    paginate = Pagination(Article.get_all_articles(), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200


@public_article.get("/search")
def article_search():
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.article_search(search_string)
    return jsonify({'error': False, 'data': data}), 200


@public_article.get("/search/title")
def title_search():
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.title_search(search_string)
    return jsonify({'error': False, 'data': data}), 200


@public_article.get("/search/body")
def body_search():
    search_string = request.args.get('search-string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search-string needed"}), 400

    data = Article.body_search(search_string)
    return jsonify({'error': False, 'data': data}), 200


@public_article.get("/pagination/article-search")
def article_search_pagination():

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
        paginate = Pagination(Article.body_search(search_string), page, limit).meta_data()
    elif search_target == "title":
        paginate = Pagination(Article.title_search(search_string), page, limit).meta_data()
    else:
        paginate = Pagination(Article.article_search(search_string), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200
