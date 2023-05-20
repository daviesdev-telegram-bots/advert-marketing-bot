from sqlalchemy import create_engine, Column, Text, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv, os
dotenv.load_dotenv()

base = declarative_base()

class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    phone = Column(String(20))
    section = Column(String(20), nullable=True, default=None)
    sub_section = Column(String(20), nullable=True, default=None)

engine = create_engine(os.getenv("DB_URL"))
connection = engine.connect()
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()