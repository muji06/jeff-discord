from os import path
import logging
from sqlalchemy import create_engine
from sqlalchemy import String, ForeignKey, Integer, JSON
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

# separate list for each user
class Watchlists(Base):
    __tablename__ = "watchlists"

    user_id = mapped_column(String(30), primary_key=True)
    watch_list = mapped_column(JSON, default=lambda: [])
    # example watch list
    # [
    #     {
    #         "from": "darvo",
    #         "waiting_for": "Kohm",
    #         "send_to": "dm",# or channel
    #         "server": "1234567890",
    #         "channel": "1234567890",
    #     }
    # ]

class Listeners(Base):
    __tablename__ = "listeners"

    listener_name = mapped_column(String(30), primary_key=True)
    current_id = mapped_column(String(30), nullable=True)
    send_to = mapped_column(JSON, default=lambda: [])
    # [
    #     {
    #         "server": "1234567890",
    #         "channel": "1234567890",
    #         "ping": "<@1234567890>"
    #     }
    # ]

def init_db():
    with engine.connect(): # just to start it
        Base.metadata.create_all(engine)
    