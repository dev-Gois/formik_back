from app import app
from flask import request
from ..views.users import post_user, get_users, get_user, update_user, delete_user
from ..views.helpers import auth
from flask_cors import cross_origin

@app.route('/users', methods=['POST', 'GET'])
@cross_origin()
def users():
    if request.method == 'POST':
        return post_user()
    else:
        return get_users()

@app.route('/users/<int:id>', methods=['PUT', 'DELETE', 'GET'])
@cross_origin()
def user(id):
    if request.method == 'PUT':
        return update_user(id)
    elif request.method == 'DELETE':
        return delete_user(id)
    else:
        return get_user(id)

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    return auth()
