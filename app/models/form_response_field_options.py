import datetime
from app import db, ma

class FormResponseFieldOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_response_field_id = db.Column(db.Integer, db.ForeignKey('form_response_fields.id'), nullable=False)
    form_field_option_id = db.Column(db.Integer, db.ForeignKey('form_field_options.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, form_response_field_id, form_field_option_id):
        self.form_response_field_id = form_response_field_id
        self.form_field_option_id = form_field_option_id

class FormResponseFieldOptionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'form_response_field_id', 'form_field_option_id')

form_response_field_option_schema = FormResponseFieldOptionsSchema()
form_response_field_options_schema = FormResponseFieldOptionsSchema(many=True)
