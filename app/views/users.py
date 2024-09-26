from app import db, app
import datetime
from werkzeug.security import generate_password_hash
from flask import jsonify, request
from ..models.users import Users, user_schema, users_schema
from jwt import encode

def post_user():
    username = request.json['username']
    password = generate_password_hash(request.json['password'])
    new_user = Users(username, password)
    try:
        db.session.add(new_user)
        db.session.commit()
        result = user_schema.dump(new_user)
        token = encode(
        {
            'id': new_user.id,
            'username': new_user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(days=7)
        },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )   
        return jsonify({'message': 'User created!', 'data': result, 'token': token, 'exp': datetime.datetime.now() + datetime.timedelta(days=7)})
    except Exception as e:
        return jsonify({'message': str(e)})

def update_user(id):
    user = Users.query.get(id)
    if user:
        user.username = request.json['username']
        user.password = generate_password_hash(request.json['password'])
        try:
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'User updated!', 'data': result})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'User not found!'})
    
def get_users():
    users = Users.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

def get_user(id):
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found!'})
    
def delete_user(id):
    user = Users.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted!'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'User not found!'})
    
def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).first()
    except:
        return None