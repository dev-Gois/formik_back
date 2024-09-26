from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.models import users 
from app.routes import users_routes
from app.models import forms
from app.models import form_fields
from app.models import form_field_options
from app.routes import forms_routes
from app.models import form_responses
from app.models import form_response_fields
from app.models import form_response_field_options
from app.routes import form_responses_routes