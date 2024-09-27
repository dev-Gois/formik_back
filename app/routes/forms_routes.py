from app import app
from flask import request
from ..views.forms import post_form, get_forms, get_form, get_user_forms, delete_form, put_form
from ..views.helpers import token_required
from flask_cors import cross_origin

@app.route('/forms', methods=['POST', 'GET'])
@cross_origin()
@token_required
def forms(current_user):
    if request.method == 'POST':
        return post_form(current_user.id)
    else:
        return get_forms()
    
@app.route('/forms/<form_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@token_required
def form(current_user, form_id):
    if request.method == 'GET':
        return get_form(form_id)
    elif request.method == 'PUT':
        return put_form(form_id)
    elif request.method == 'DELETE':
        return delete_form(form_id)
    
@app.route('/users/<user_id>/forms', methods=['GET'])
@cross_origin()
@token_required
def user_forms(user_id):
    return get_user_forms(user_id)


