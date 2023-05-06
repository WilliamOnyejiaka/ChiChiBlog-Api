from flask import Blueprint, jsonify, request
from typing import Dict
from werkzeug.security import generate_password_hash, check_password_hash
from src.config import DEFAULT_MAIN_ADMIN_PASS
from src.api.models.Admin import Admin
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.modules.valid_object_id import valid_object_id

main_admin = Blueprint("main_admin",__name__,url_prefix="/api/main-admin")


@main_admin.get("/create-main-admin")
def create_main_admin():
    password_hash = generate_password_hash(DEFAULT_MAIN_ADMIN_PASS)

    if Admin.get_admin_by_type("main"):
        return jsonify({
            'error': True,
            'message': "admin type already exists"
        }), 400

    admin: Dict = {
        'name': "ChiChi",
        'password': password_hash,
        'type': "main",
        'email': "chichi@email.com"
    }

    if Admin.create_admin(admin):

        return jsonify({
            'error': False,
            'message': "default main admin created successfully"
        }), 201

    return jsonify({
        'error': True,
        'message': "something went wrong"
    }), 500


@main_admin.get('/token/admin-token')
@jwt_required()
def admin_token():
    admin_id = get_jwt_identity()
    admin = Admin.get_admin_by_id(admin_id)

    if admin:
        if admin['type'] == "main":
            token = create_access_token(identity="main")

            return jsonify({
                'error': False,
                'admin_token': token
            }), 201

        return jsonify({
            'error': True,
            'message': "admin not authorized"
        }), 401

    return jsonify({
        'error': True,
        'message': "admin does not exists"
    }), 404

@main_admin.delete('/delete/delete-admin')
@jwt_required()
def delete_admin():
    admin_id = get_jwt_identity()
    admin = Admin.get_admin_by_id(admin_id)

    if admin:
        if admin['type'] == "main":

            return jsonify({
                'error': False,
                'message': "admin deleted successfully"
            }), 200

        return jsonify({
            'error': True,
            'message': "admin not authorized"
        }), 401

    return jsonify({
        'error': True,
        'message': "admin does not exists"
    }), 404
