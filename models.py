from sqlalchemy import Column,Integer,String,Float,Date
from db import Base,engine


class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    height= Column(Float)

class WeightEntry(Base):
    __tablename__="Weight_entries"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    weight= Column(Float)
    date= Column(Date) 


Base.metadata.create_all(bind=engine)