import datetime 
import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, 
                           primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True, unique=True)
    email = sa.Column(sa.String, 
                              index=True, unique=True, nullable=True)
    hashed_password = sa.Column(sa.String)
    created_date = sa.Column(sa.DateTime, 
                                     default=datetime.datetime.now)