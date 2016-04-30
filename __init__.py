from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# Migrations
migrate = Migrate(app,db)

# Markdown
Markdown(app)

from blog import views
from author import views
