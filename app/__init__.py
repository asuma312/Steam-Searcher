from app.db.setup import engine, Base
from app.models.sql import AppDetail, AppId
Base.metadata.create_all(bind=engine)