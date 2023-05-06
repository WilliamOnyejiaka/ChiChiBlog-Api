from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config import SECRET_KEY,JWT_ACCESS_TOKEN_EXPIRES,JWT_QUERY_STRING_NAME,JWT_REFRESH_TOKEN_EXPIRES,JWT_SECRET_KEY,JWT_TOKEN_LOCATION
from src.api.routes.admin import admin
from src.api.routes.article import article
from src.api.routes.main_admin import main_admin


def create_app():

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        JWT_SECRET_KEY=JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=JWT_ACCESS_TOKEN_EXPIRES,
        JWT_REFRESH_TOKEN_EXPIRES=JWT_REFRESH_TOKEN_EXPIRES,
        JWT_TOKEN_LOCATION=JWT_TOKEN_LOCATION,
        JWT_QUERY_STRING_NAME=JWT_QUERY_STRING_NAME
    )

    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": {
                "*",
            }
        }
    })

    JWTManager(app)

    app.register_blueprint(admin)
    app.register_blueprint(article)
    app.register_blueprint(main_admin)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            'error':True,
            'message':"Not Found"
        })

    return app
