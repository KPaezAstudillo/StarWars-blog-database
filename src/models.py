import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String(250))
    eye_color = Column(String(250))


class Planet(Base):
    __tablename__= 'planets'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    diameter = Column(Integer)
    

class FavoriteCharacter(Base):
    __tablename__= 'favoritecharacters'
    users_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    characters_id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    user = relationship('User')

class FavoritePlanet(Base):
    __tablename__= 'favoriteplanets'
    users_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    planets_id = Column(Integer, ForeignKey('planets.id'), primary_key=True)
    user = relationship('User')
    

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
