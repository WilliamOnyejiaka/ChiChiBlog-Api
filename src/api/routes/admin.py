from flask import Blueprint,jsonify,request
from typing import Dict
from werkzeug.security import generate_password_hash,check_password_hash
from src.config import DEFAULT_MAIN_ADMIN_PASS
from src.api.models.Admin import Admin
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
import validators
from src.modules.valid_object_id import valid_object_id


admin = Blueprint("admin",__name__,url_prefix="/api/admin")   

@admin.get('/login')
def login():
    email = request.authorization.get('username',None)
    password = request.authorization.get('password',None)

    if not email and not password:
        return jsonify({
            'error':True,
            'message':"email and password are needed"
        }),400

    current_admin = Admin.get_admin_by_email(email.strip())

    if current_admin:
        valid_password = check_password_hash(current_admin['password'],password)
        if valid_password:
            access_token = create_access_token(identity=current_admin['_id'])
            refresh_token = create_refresh_token(identity=current_admin['_id'])
            data = {
                '_id': current_admin['_id'],
                'name': current_admin['name'],
                'email': current_admin['email'],
                'type': current_admin['type'],
                'created_at': current_admin['created_at'],
                'updated_at': current_admin['updated_at']
            }

            return jsonify({
                'error': False,
                'message': "logged in successfully",
                'data': data,
                'token':{
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }),200
        
        return jsonify({
            'error': True,
            'message': "invalid password"
        }),400
    
    return jsonify({
        'error':True,
        'message':"admin does not exists"
    }),404

@admin.post("/create-admin")
@jwt_required()
def create_admin():
    identity = get_jwt_identity()

    if identity == "main":
        name = request.get_json().get('name', None)
        password = request.get_json().get('password', None)
        email = request.get_json().get('email', None)

        if not name or not password or not email:
            return jsonify({
                'error': True,
                'message': "all values needed"
            }), 400

        if len(name) < 2:
            return jsonify({
                'error': True,
                'message': "name length is less than 2"
            }), 400
        
        if len(password) < 5:
            return jsonify({
                'error': True,
                'message': "password length is less than 5"
            }), 400
        
        if not validators.email(email):
            return jsonify({
                'error':True,
                'message':"invalid email"
            }), 400
        
        if Admin.get_admin_by_email(email):
            return jsonify({
                'error': True,
                'message': "email already exists"
            }), 400
        
        password_hash = generate_password_hash(password)
        
        if Admin.create_admin({
            'name': name,
            'password': password_hash,
            'email': email,
            'type': "sub"
        }):
            return jsonify({
                'error': False,
                'message': "admin created successfully"
            }), 201

        return jsonify({
            'error': True,
            'message': "something went wrong"
        }), 500
    
    return jsonify({
        'error': True,
        'message': "not authorized"
    }),401

@admin.patch("/update/password")
@jwt_required()
def update_admin_password():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    password = request.get_json().get('password',None)
    new_password = request.get_json().get('new_password',None)
    current_admin = Admin.get_admin_by_id(admin_id)

    if not current_admin:
        return jsonify({
            'error':True,
            'message': "admin does not exists"
        }),401
    
    if not password or not new_password:
        return jsonify({
            'error': True,
            'message': "all values needed"
        }),400

    valid_password = check_password_hash(current_admin['password'], password)

    if valid_password:
        if len(new_password) < 5:
            return jsonify({
                'error': True,
                'message': "password length is less than 5"
            }), 400
        
        password_hash = generate_password_hash(new_password)

        if Admin.update_admin_password(admin_id,password_hash):
            return jsonify({
                'error': False,
                'message': "password has been updated successfully"
            }),200
        
        return jsonify({
            'error': True,
            'message': "something went wrong"
        }), 500
    
    return jsonify({
        'error': True,
        'message': "invalid password"
    }), 401


@admin.patch("/update/email")
@jwt_required()
def update_admin_email():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    new_email = request.get_json().get('new_email', None)
    current_admin = Admin.get_admin_by_id(admin_id)

    if not new_email:
        return jsonify({
            'error': True,
            'message': "new email required"
        }), 400

    if not current_admin:
        return jsonify({
            'error': True,
            'message': "admin does not exists"
        }), 401

    if Admin.get_admin_by_email(new_email):
        return jsonify({
            'error': False,
            'message': "email already in use"
        }), 400

    if validators.email(new_email):
        if Admin.update_admin_email(admin_id,new_email):
            return jsonify({
                'error': False,
                'message': "email has been updated successfully"
            }), 200
        
        return jsonify({
            'error': True,
            'message': "something went wrong"
        }), 500
    
    return jsonify({
        'error':True,
        'message': "new email is invalid"
    }),400

@admin.patch("/update/name")
@jwt_required()
def update_admin_name():
    admin_id = get_jwt_identity()

    if not valid_object_id(admin_id):
        return jsonify({
            'error': True,
            'message': "access token needed"
        }), 401

    new_name = request.get_json().get('new_name',None)

    if not new_name:
        return jsonify({
            'error': True,
            'message': "new name required"
        }),400

    current_admin = Admin.get_admin_by_id(admin_id)
    
    if not current_admin:
        return jsonify({
            'error': True,
            'message': "admin does not exists"
        }), 401

    if len(new_name) < 2:
        return jsonify({
            'error': True,
            'message': "new name length is less than 2"
        }), 400
    
    if Admin.update_admin_name(admin_id,new_name):
        return jsonify({
            'error': False,
            'message': "name has been updated successfully"
        }),200
    
    return jsonify({
        'error': True,
        'message': "something went wrong"
    }),500


@admin.get('/token/access-token')
@jwt_required(refresh=True)
def admin_token():
    admin_id = get_jwt_identity()
    admin = Admin.get_admin_by_id(admin_id)

    if admin:
        token = create_access_token(identity=admin_id)

        return jsonify({
            'error': False,
            'admin_token': token
        }), 201

    return jsonify({
        'error': True,
        'message': "admin does not exists"
    }), 404


@admin.get("/test")
@jwt_required()
def test():
    identity = get_jwt_identity()

    try:

        print(ObjectId("main"))
    except:
        print("not valid")
    return jsonify({
        'error': False,
        'message': identity
    }),200
