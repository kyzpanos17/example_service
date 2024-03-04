from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from app.models import db
from flasgger import Swagger

# initialize App
app = Flask(__name__)

# initialize Swagger API
swagger = Swagger(app, template_file="API/api_specification.yaml")

# Configure logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)  # Set the log level to DEBUG to log all messages
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Choose configuration setting
app.config.from_object('config.development')

# initialize
db.init_app(app)

# Setup Database
with app.app_context():
    db.create_all()



