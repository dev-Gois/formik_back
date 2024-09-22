import datetime
from app import db, ma

class FormFields(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum('short_answer', 'long_answer', 'multiple_choice', 'single_choice'), nullable=False)
    required = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    options = db.relationship('FormFieldOptions', backref='field', lazy=True)

    def __init__(self, form_id, name, type, required):
        self.form_id = form_id
        self.name = name
        self.type = type
        self.required = required

class FormFieldsSchema(ma.Schema):
    options = ma.Nested('FormFieldOptionsSchema', many=True)

    class Meta:
        fields = ('id', 'form_id', 'name', 'type', 'required', 'options', 'created_at')

form_field_schema = FormFieldsSchema()
form_fields_schema = FormFieldsSchema(many=True)