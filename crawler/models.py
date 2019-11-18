from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings
import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class MusicList(DeclarativeBase):
    __tablename__ = "t_music_list"
    mlid = Column('mid', Integer, primary_key=True)
    name = Column('name', String(128))  # 歌单名称
    description = Column('description', Text)  # 歌单描述
    created = Column('created', DateTime(), default=datetime.datetime.utcnow)


class Music(DeclarativeBase):
    __tablename__ = "t_music"
    mid = Column('mid', Integer, primary_key=True)
    name = Column('name', String(128))  # 歌曲名称
    url = Column('url', String(256))  # 歌曲文件链接
    created = Column('created', DateTime(), default=datetime.datetime.utcnow)
