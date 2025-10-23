from flask import *
from sqlalchemy import text



def create_app():
    app = Flask(__name__)
    from flask_cors import CORS
    from app.routes import api_bp
    from app.db import db_path
    import duckdb
    CORS(app)
    from app.db.setup import engine, Base, get_db
    from app.models.sql import AppDetail, AppId
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        # duckdb doesnt have materialized views
        conn.execute(text(
            """
            CREATE VIEW IF NOT EXISTS app_genres AS
            SELECT DISTINCT element AS genre
            FROM detail,
                 UNNEST(genres) AS element
            """
        )
        )

        conn.execute(text(
            """
            CREATE VIEW IF NOT EXISTS app_categories AS
            SELECT DISTINCT element AS category
            FROM detail,
                 UNNEST(categories) AS element
            """)
        )
    engine.dispose()
    app.register_blueprint(api_bp)
    return app