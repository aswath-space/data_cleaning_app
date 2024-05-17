from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the base class for declarative models
Base = declarative_base()

# Example table definition using SQLAlchemy ORM
class ExampleTable(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

def create_schema(engine):
    """
    Create all tables defined in the ORM classes.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.

    Returns:
    - None
    """
    Base.metadata.create_all(engine)
    logger.info("Schema created successfully.")

def drop_schema(engine):
    """
    Drop all tables defined in the ORM classes.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.

    Returns:
    - None
    """
    Base.metadata.drop_all(engine)
    logger.info("Schema dropped successfully.")
