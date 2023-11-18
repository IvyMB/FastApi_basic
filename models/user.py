from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    birthday = Column(String)
    gender = Column(String)
    country = Column(String)
    languages = Column(JSON)
