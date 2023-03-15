import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    game = sa.Column(sa.String)
