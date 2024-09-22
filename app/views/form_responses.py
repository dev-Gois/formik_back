from app import db
from flask import jsonify, request
from ..models.form_responses import FormResponses, form_response_schema, form_responses_schema
from ..models.form_response_fields import FormResponseFields, form_response_field_schema, form_response_fields_schema
from ..models.form_response_field_options import FormResponseFieldOptions, form_response_field_option_schema, form_response_field_options_schema
from ..models.forms import Forms, forms_schema, form_schema
from ..models.form_fields import FormFields, form_field_schema, form_fields_schema
from ..models.form_field_options import FormFieldOptions, form_field_option_schema, form_field_options_schema

def get_form_responses(form_id):
    form_responses = FormResponses.query.filter_by(form_id=form_id).all()
    return jsonify(form_responses_schema.dump(form_responses))

def get_form_response(form_response_id):
    form_response = FormResponses.query.get(form_response_id)
    return jsonify(form_response_schema.dump(form_response))

def create_form_response(form_id, user_id):
    new_form_response = FormResponses(form_id, user_id)
    try:
        db.session.add(new_form_response)
        db.session.commit()
        fields = request.json['fields']
        for field in fields:
            form_field = FormFields.query.get(field['id'])

            if form_field.type in ['multiple_choice', 'single_choice']:
                new_response_field = FormResponseFields(new_form_response.id, field['id'], None, None)
                db.session.add(new_response_field)
                db.session.commit()
                for option in field['options']:
                    new_response_field_option = FormResponseFieldOptions(new_response_field.id, option)
                    db.session.add(new_response_field_option)
                    db.session.commit()
            else:
                response = field['response']
                if form_field.type == 'short_answer':
                    new_response_field = FormResponseFields(new_form_response.id, field['id'], response, None)
                else:
                    new_response_field = FormResponseFields(new_form_response.id, field['id'], None, response)
                db.session.add(new_response_field)
                db.session.commit()
                                    
        return jsonify({'message': 'Form response created!', 'form_response': form_response_schema.dump(new_form_response)})
    except Exception as e:
        return jsonify({'message': str(e)})
