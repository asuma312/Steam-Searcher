from app.db.setup import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, JSON
from app.models.crawlers import AppIdResponse
from sqlalchemy.orm import sessionmaker, Session, relationship
from app.utils.logger import logger
class AppId(Base):
    __tablename__ = 'app_id'
    app_id = Column(Integer, primary_key=True, autoincrement=False)
    app_name = Column(Text, nullable=False)

    app_info = relationship("AppDetail", back_populates="app_id")

    @classmethod
    def from_pydantic(cls, pydantic_detail: AppIdResponse, db_session: Session, low_memory:bool = False):
        app_list = pydantic_detail.applist
        added_classes = []
        if low_memory:
            for app in app_list.apps:
                existing_app = db_session.query(cls).filter_by(app_id=app.appid).first()
                if not existing_app:
                    new_app = cls(
                        app_id=app.app_id,
                        app_name=app.name
                    )
                    added_classes.append(new_app)
                    db_session.add(new_app)
                else:
                    logger.info(f"App with ID {app.appid} already exists in the database, skipping addition.")
        else:
            # use in memory instead of database single query
            _old_app_list = db_session.query(cls).all()
            for app in app_list.apps:
                existing_app = next((a for a in _old_app_list if a.app_id == app.appid), None)
                if not existing_app:
                    new_app = cls(
                        app_id=app.appid,
                        app_name=app.name
                    )
                    added_classes.append(new_app)
                    db_session.add(new_app)
                else:
                    logger.info(f"App with ID {app.appid} already exists in the database, skipping addition.")
        return added_classes
