from jwt import decode, encode
import datetime
from werkzeug.security import check_password_hash
from flask import jsonify, request
from functools import wraps
from .users import user_by_username
from app import app

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify!', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401

    user = user_by_username(auth.username)
    if not user:
        return jsonify({'message': 'User not found!'}), 401
    
    if user and check_password_hash(user.password, auth.password):
        token = encode(
                {
                    'id': user.id,
                    'username': user.username,
                    'exp': datetime.datetime.now() + datetime.timedelta(days=7)
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

        return jsonify({'message': 'Validate successfully!', 'token': token, 'exp': datetime.datetime.now() + datetime.timedelta(days=7)})
    
    return jsonify({'message': 'Could not verify!', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!', 'data': {}}), 401
        try:
            data = decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_by_username(data['username'])
        except:
            return jsonify({'message': 'Token is invalid!', 'data': {}}), 401
        return f(current_user, *args, **kwargs)
    return decorated
