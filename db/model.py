"""
SQLAlchemy model for the data table
"""
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.environment import DATABASE_URL, TABLE_NAME

Base = declarative_base()

class DataTable(Base):
    __tablename__ = TABLE_NAME
    
    id = Column(Integer, primary_key=True)
    column_1 = Column(Integer)
    column_2 = Column(Integer)
    column_3 = Column(Integer)
    column_4 = Column(Integer)
    column_5 = Column(Integer)


# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
