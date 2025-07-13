from flask import *
from flask_cors import CORS
from app.routes import api_bp
def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api_bp)
    return app