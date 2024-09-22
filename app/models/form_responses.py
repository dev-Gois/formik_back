import datetime
from app import db, ma
from .form_response_fields import FormResponseFieldsSchema
from .forms import FormsSchema

class FormResponses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now) 

    def __init__(self, form_id, user_id):
        self.form_id = form_id
        self.user_id = user_id

class FormResponsesSchema(ma.Schema):
    form = ma.Nested(FormsSchema)
    fields = ma.Nested(FormResponseFieldsSchema, many=True)

    class Meta:
        fields = ('id', 'form_id', 'user_id', 'created_at')

form_response_schema = FormResponsesSchema()
form_responses_schema = FormResponsesSchema(many=True)