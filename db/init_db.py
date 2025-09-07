"""
Database initialization and seeding
"""
import random
from sqlalchemy import inspect
from .model import Base, engine, DataTable, SessionLocal
from config.environment import TABLE_NAME
from config.logging_config import logger
from config.columns import get_columns_names

def init_database():
    """Initialize database with table creation and seed data"""
    # Check if table already exists
    inspector = inspect(engine)
    if inspector.has_table(TABLE_NAME):
        logger.info(f"Table '{TABLE_NAME}' already exists, skipping initialization")
        return
    
    # Create table
    Base.metadata.create_all(bind=engine)
    logger.info(f"Created table '{TABLE_NAME}'")
    
    # Seed with random data
    seed_data()

def seed_data():
    """Add random data to the table"""
    session = SessionLocal()
    
    # Add 10 rows with random integer values
    for i in range(10):
        # Create row data dynamically based on column configuration
        row_data = {}
        for column_name in get_columns_names():
            row_data[column_name] = random.randint(1, 100)
        
        row = DataTable(**row_data)
        session.add(row)
    
    session.commit()
    session.close()
    logger.info("Seeded database with random data")
