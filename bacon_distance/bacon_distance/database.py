from typing import Any, Generator
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    mapped_column,
    relationship,
    sessionmaker,
)

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:password@db:3306/bacon_distance")
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class ActorMovie(Base):
    __tablename__ = "actor_movie"
    actor_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("actors.nconst"), primary_key=True
    )
    movie_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("movies.tconst"), primary_key=True
    )

    actor = relationship("Actor", back_populates="actor_movies")
    movie = relationship("Movie", back_populates="actor_movies")


class Actor(Base):
    __tablename__ = "actors"
    nconst: Mapped[str] = mapped_column(String(255), primary_key=True)
    primaryName: Mapped[str] = mapped_column(String(255), nullable=False)

    actor_movies = relationship("ActorMovie", back_populates="actor")


class Movie(Base):
    __tablename__ = "movies"
    tconst: Mapped[str] = mapped_column(String(255), primary_key=True)
    primaryTitle: Mapped[str] = mapped_column(String(255), nullable=False)

    actor_movies = relationship("ActorMovie", back_populates="movie")


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db() -> Session:
    """
    method to connect to the db than drop the old tables and create new ones
    :return: the session to the db
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
    return SessionLocal()
