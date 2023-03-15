import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    login = sa.Column(sa.String, unique=True, index=True, primary_key=True)
    hashed_password = sa.Column(sa.String)
    count = sa.Column(sa.Integer, default=0)