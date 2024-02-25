from os import path
import logging
from sqlalchemy import create_engine
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger(__name__)

DATABASE_PATH = "/data/jeff.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)


class Base(DeclarativeBase):
    pass


class Watchlists(Base):
    __tablename__ = "watchlists"

    user_id = mapped_column(String(30), primary_key=True)
    server_id = mapped_column(String(20), primary_key=True)
    watch_list = mapped_column(String(30), nullable=True)
    total_videos = mapped_column(Integer, default=0)
    total_storage = mapped_column(Integer,  default=0)

class Listeners(Base):
    __tablename__ = "listeners"

    listener_id = mapped_column(String(30), primary_key=True)
    current_id = mapped_column(String(30), nullable=True)
    __
def init_db():
    with engine.connect(): # just to start it
        Base.metadata.create_all(engine)
    