from app import db
from flask import jsonify, request
from ..models.forms import Forms, form_schema, forms_schema
from ..models.form_fields import FormFields, form_field_schema, form_fields_schema
from ..models.form_field_options import FormFieldOptions, form_field_option_schema, form_field_options_schema

def post_form(user_id):
    title = request.json['title']
    description = request.json['description']
    new_form = Forms(user_id, title, description)
    try:
        db.session.add(new_form)
        db.session.commit()
        fields = request.json['fields']
        for field in fields:
            new_field = FormFields(new_form.id, field['name'], field['type'], field['required'])
            db.session.add(new_field)
            db.session.commit()
            if field['type'] in ['multiple_choice', 'single_choice']:
                options = field['options']
                for option in options:
                    new_option = FormFieldOptions(new_field.id, option['name'])
                    db.session.add(new_option)
                    db.session.commit()
        return jsonify({'message': 'Form created!', 'form': form_schema.dump(new_form)})
    except Exception as e:
        return jsonify({'message': str(e)})
    
def get_forms():
    all_forms = Forms.query.all()
    result = forms_schema.dump(all_forms)
    return jsonify(result)

def get_form(form_id):
    form = Forms.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form not found!'}), 404
    return jsonify(form_schema.dump(form))

def get_user_forms(user_id):
    user_forms = Forms.query.filter_by(user_id=user_id).all()
    result = forms_schema.dump(user_forms)
    return jsonify(result)

def delete_form(form_id):
    form = Forms.query.get(form_id)
    
    if not form:
        return jsonify({'message': 'Form not found!'}), 404

    try:
        fields = FormFields.query.filter_by(form_id=form_id).all()
        
        for field in fields:
            options = FormFieldOptions.query.filter_by(form_field_id=field.id).all()
            for option in options:
                db.session.delete(option)
            db.session.delete(field)
        
        # Exclui o formulário
        db.session.delete(form)
        db.session.commit()
        
        return jsonify({'message': 'Form deleted!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


def put_form(form_id):
    form = Forms.query.get(form_id)
    form.title = request.json['title']
    form.description = request.json['description']
    db.session.commit()
    fields = request.json['fields']
    for field in fields:
        if 'id' in field:
            field_to_update = FormFields.query.get(field['id'])
            field_to_update.name = field['name']
            field_to_update.type = field['type']
            field_to_update.required = field['required']
            db.session.commit()
            if field['type'] in ['multiple_choice', 'single_choice']:
                options = field['options']
                for option in options:
                    if 'id' in option:
                        option_to_update = FormFieldOptions.query.get(option['id'])
                        option_to_update.name = option['name']
                        db.session.commit()
                    else:
                        new_option = FormFieldOptions(field_to_update.id, option['name'])
                        db.session.add(new_option)
                        db.session.commit()
        else:
            new_field = FormFields(form_id, field['name'], field['type'], field['required'])
            db.session.add(new_field)
            db.session.commit()
            if field['type'] in ['multiple_choice', 'single_choice']:
                options = field['options']
                for option in options:
                    new_option = FormFieldOptions(new_field.id, option['name'])
                    db.session.add(new_option)
                    db.session.commit()
    return jsonify({'message': 'Form updated!', 'form': form_schema.dump(form)})