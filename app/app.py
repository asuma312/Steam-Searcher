from flask import *
from flask_cors import CORS
from app.routes import api_bp
from app.db import db_path
import duckdb
def create_app():
    app = Flask(__name__)
    CORS(app)
    with duckdb.connect(db_path) as conn:
        # duckdb doesnt have materialized views
        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS app_genres AS
            SELECT DISTINCT element AS genre
            FROM detail,
                 UNNEST(genres) AS element
            """
        )

        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS app_categories AS
            SELECT DISTINCT element AS category
            FROM detail,
                 UNNEST(categories) AS element
            """
        )
    app.register_blueprint(api_bp)
    return app