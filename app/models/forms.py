import datetime
from app import db, ma
from .form_fields import FormFieldsSchema

class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now) 

    fields = db.relationship('FormFields', backref='form', lazy=True)

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description

class FormsSchema(ma.Schema):
    fields = ma.Nested(FormFieldsSchema, many=True)

    class Meta:
        fields = ('id', 'user_id', 'title', 'description', 'fields', 'created_at')

# quero que o form schema tenha os campos do form e os campos dos fields

form_schema = FormsSchema()
forms_schema = FormsSchema(many=True)


