import datetime
from app import db, ma

class FormFieldOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_field_id = db.Column(db.Integer, db.ForeignKey('form_fields.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, form_field_id, name):
        self.form_field_id = form_field_id
        self.name = name

class FormFieldOptionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'form_field_id', 'name', 'created_at')

form_field_option_schema = FormFieldOptionsSchema()
form_field_options_schema = FormFieldOptionsSchema(many=True)