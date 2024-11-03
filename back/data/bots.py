import datetime
import sqlalchemy
import json
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Bot(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'bots'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
    					    index=True, nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String,
                            index=True, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String,
                            index = True, nullable=False, default='')
    
    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description
        