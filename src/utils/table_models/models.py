from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(Text, nullable=False, unique=True)


class Language(Base):
    __tablename__ = 'languages'

    language_id = Column(Integer, primary_key=True)
    language_name = Column(Text, nullable=False, unique=True)


class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    imdb_id = Column(Integer, nullable=False, unique=True)
    title = Column(Text, nullable=False)
    release_year = Column(SmallInteger)
    duration = Column(Integer)
    budget = Column(NUMERIC(15, 2))
    box_office = Column(NUMERIC(15, 2))
    description = Column(Text)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    language_id = Column(Integer, ForeignKey('languages.language_id'))
    mpaa_rating = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, default=datetime.utcnow())

    country = relationship('Country')
    language = relationship('Language')


class MovieCrew(Base):
    __tablename__ = 'movies_crew'

    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    person_id = Column(
        Integer,
        ForeignKey('movies_people.person_id'),
        primary_key=True,
    )
    role_id = Column(Integer, ForeignKey('movies_roles.role_id'), nullable=False)

    movie = relationship('Movie')
    person = relationship('MoviesPerson')
    role = relationship('MoviesRole')


# Таблица жанров фильмов
class MovieGenreList(Base):
    __tablename__ = 'movie_genres_list'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(Text, nullable=False, unique=True)


# Таблица связи фильмов с жанрами
class MovieGenreAssociation(Base):
    __tablename__ = 'movie_genres_association'

    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    genre_id = Column(
        Integer,
        ForeignKey('movie_genres_list.genre_id'),
        primary_key=True,
    )

    movie = relationship('Movie')
    genre = relationship('MovieGenreList')


# Таблица людей (актеров, режиссеров и др.)
class MoviesPerson(Base):
    __tablename__ = 'movies_people'

    person_id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    birth_date = Column(Date)


# Таблица ролей (актер, режиссер и т.д.)
class MoviesRole(Base):
    __tablename__ = 'movies_roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(Text, nullable=False, unique=True)


class MovieSource(Base):
    __tablename__ = 'movies_sources'

    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    imdb_id = Column(Integer, nullable=False)
    dataset_name = Column(String(50), primary_key=True)
    original_id = Column(Integer, primary_key=True)

    movie = relationship('Movie', backref='sources')

    __table_args__ = (
        UniqueConstraint(
            'movie_id',
            'dataset_name',
            'original_id',
            name='_movie_source_uc',
        ),
    )
