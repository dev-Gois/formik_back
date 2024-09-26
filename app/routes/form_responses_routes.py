from app import app
from flask import request
from ..views.form_responses import get_form_responses, get_form_response, create_form_response
from ..views.helpers import token_required
from flask_cors import cross_origin

@app.route('/forms/<form_id>/responses', methods=['POST', 'GET'])
@cross_origin()
@token_required
def form_responses(current_user, form_id):
    if request.method == 'POST':
        return create_form_response(form_id, current_user.id)
    else:
        return get_form_responses(form_id)

@app.route('/responses/<form_response_id>', methods=['GET'])
@cross_origin()
@token_required
def form_response(form_response_id):
    return get_form_response(form_response_id)
