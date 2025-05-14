import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Character(SqlAlchemyBase):
    __tablename__ = 'characters_table'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    c_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    c_class = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    c_race = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    c_characteristics = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    c_about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)