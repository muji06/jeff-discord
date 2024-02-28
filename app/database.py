from os import path
import logging
from sqlalchemy import create_engine
from sqlalchemy import String, JSON
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

# Users can subscribe to get DMs from the bot when certain event happens
class Watchlists(Base):
    __tablename__ = "watchlists"

    user_id = mapped_column(String(30), primary_key=True)
    watch_list = mapped_column(JSON, default=lambda: [])
    # example watch list
    # [
    #     {
    #         "type": "darvo",
    #         "target": "Kohm",
    #     },
    #     {
    #         "type": "darvo",
    #         "target": "Kohm",
    #         "price": 40
    #      },
    #     {
    #         "type": "fissure",
    #         "target": "axi",
    #         "mode": "capture",
    #      }
    # ]

# Each server admin can set up events to be shown server-wide on specific channel
class Listeners(Base):
    __tablename__ = "listeners"
    
    server_id = mapped_column(String(30), primary_key=True)
    listeners = mapped_column(JSON, default=lambda: [])
    # [
    #     {
    #         
    #         "server": "1234567890",
    #         "channel": "1234567890",
    #         "ping": "<@1234567890>"
    #     }
    # ]

class Events(Base):
    __tablename__ = "events"

    event = mapped_column(String(30), primary_key=True)
    rotation_metadata = mapped_column(JSON, default=lambda: {"id": None, "ends_at": None})

def init_db():
    with engine.connect(): # just to start it
        Base.metadata.create_all(engine)
    