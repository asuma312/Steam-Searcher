from app.db.setup import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, JSON, ForeignKey
from app.models.crawlers import AppDetail as PyDanticAppDetail
from sqlalchemy.orm import sessionmaker, Session, relationship
from bs4 import BeautifulSoup


class AppDetail(Base):
    __tablename__ = "detail"
    steam_appid = Column(Integer, ForeignKey('app_id.app_id'), nullable=False, unique=True, autoincrement=False, primary_key=True)
    type = Column(String)
    name = Column(String)
    required_age = Column(Integer)
    is_free = Column(Boolean)

    dlc = Column(JSON)
    detailed_description = Column(Text)
    about_the_game = Column(Text)
    short_description = Column(Text)
    supported_languages = Column(Text)
    header_image = Column(String)
    website = Column(String)

    pc_requirements = Column(JSON)
    mac_requirements = Column(JSON)
    linux_requirements = Column(JSON)

    developers = Column(JSON)
    publishers = Column(JSON)
    price_overview = Column(JSON)
    packages = Column(JSON)
    platforms = Column(JSON)
    metacritic = Column(JSON)
    categories = Column(JSON)
    genres = Column(JSON)
    screenshots = Column(JSON)
    movies = Column(JSON)
    recommendations = Column(JSON)
    achievements = Column(JSON)
    release_date = Column(JSON)
    support_info = Column(JSON)
    background = Column(String)
    content_descriptors = Column(JSON)
    tags = Column(JSON)

    app_id = relationship("AppId", back_populates="app_info")

    @classmethod
    def from_pydantic(cls, pydantic_detail: PyDanticAppDetail, db_session: Session):
        if not isinstance(pydantic_detail, PyDanticAppDetail):
            raise TypeError("O input deve ser uma instância de AppDetail Pydantic.")


        detailed_description = pydantic_detail.detailed_description
        try:
            soup = BeautifulSoup(detailed_description, 'html.parser')
            detailed_description = soup.get_text()
        except:detailed_description = pydantic_detail.detailed_description

        app_detail_sql = cls(
            steam_appid=pydantic_detail.steam_appid,
            type=pydantic_detail.type,
            name=pydantic_detail.name,
            required_age=pydantic_detail.required_age,
            is_free=pydantic_detail.is_free,
            dlc=pydantic_detail.dlc,
            detailed_description=detailed_description,
            about_the_game=pydantic_detail.about_the_game,
            short_description=pydantic_detail.short_description,
            supported_languages=pydantic_detail.supported_languages,
            header_image=pydantic_detail.header_image,
            website=pydantic_detail.website,
            developers=pydantic_detail.developers,
            publishers=pydantic_detail.publishers,
            price_overview=pydantic_detail.price_overview,
            packages=pydantic_detail.packages,
            platforms=pydantic_detail.platforms,
            metacritic=pydantic_detail.metacritic,
            categories=pydantic_detail.categories,
            genres=pydantic_detail.genres,
            screenshots=pydantic_detail.screenshots,
            movies=pydantic_detail.movies,
            recommendations=pydantic_detail.recommendations,
            achievements=pydantic_detail.achievements,
            release_date=pydantic_detail.release_date,
            support_info=pydantic_detail.support_info,
            background=pydantic_detail.background,
            content_descriptors=pydantic_detail.content_descriptors,
            tags=pydantic_detail.tags,
            linux_requirements_json=pydantic_detail.linux_requirements.json() if pydantic_detail.linux_requirements else None,
            mac_requirements_json=pydantic_detail.mac_requirements.json() if pydantic_detail.mac_requirements else None,
            pc_requirements_json=pydantic_detail.pc_requirements.json() if pydantic_detail.pc_requirements else None
        )
        db_session.add(app_detail_sql)

        return app_detail_sql