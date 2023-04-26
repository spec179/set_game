import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    game = sa.Column(sa.String)
