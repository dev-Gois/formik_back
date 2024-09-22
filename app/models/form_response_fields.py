import datetime
from app import db, ma

from .form_response_field_options import FormResponseFieldOptionsSchema

class FormResponseFields(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_response_id = db.Column(db.Integer, db.ForeignKey('form_responses.id'), nullable=False)
    form_field_id = db.Column(db.Integer, db.ForeignKey('form_fields.id'), nullable=False)
    short_response = db.Column(db.String(200), nullable=True)
    long_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, form_response_id, form_field_id, response):
        self.form_response_id = form_response_id
        self.form_field_id = form_field_id
        self.response = response

class FormResponseFieldsSchema(ma.Schema):
    options = ma.Nested(FormResponseFieldOptionsSchema, many=True)

    class Meta:
        fields = ('id', 'form_response_id', 'form_field_id', 'response', 'options', 'created_at')

form_response_field_schema = FormResponseFieldsSchema()
form_response_fields_schema = FormResponseFieldsSchema(many=True)
