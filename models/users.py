from sqlalchemy import Column, Integer, String
from .bdCreator import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)

    def __init__(self, url, status):
        self.url = url
        self.status = status
