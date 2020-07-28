from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy.schema import FetchedValue

from flask_login import UserMixin

from app import db

class BaseModel(db.Model):
    """Base data model for all objects."""
    __abstract__ = True

class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(150))
    name = Column(String(75))
    surname = Column(String(75))
    password = Column(String(100))

    def __repr__(self):
        return f'User {self.id}: {self.email}, {self.name}, {self.surname}'

class Flight(BaseModel):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    airline = Column(String(6))
    flight_no = Column(String(8))
    dep = Column(String(10))
    dest = Column(String(10))
    acft_reg = Column(String(8))
    status = Column(String(14), default='Not calculated')

class Planet(BaseModel):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True)
    name = Column(String(10))

    def __repr__(self):
        return f'Planet {self.id}: {self.name}'