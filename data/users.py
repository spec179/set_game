import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    login = sa.Column(sa.String, unique=True, index=True, primary_key=True)
    hashed_password = sa.Column(sa.String)
    count = sa.Column(sa.Integer, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)