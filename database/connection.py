from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_engine(db_type, host, port, username, password, db_name):
    """
    Create a SQLAlchemy engine for the specified database type.
    
    Parameters:
    - db_type (str): The type of the database (e.g., 'sqlite', 'postgresql', 'mysql', 'mssql', 'oracle').
    - host (str): The database server host.
    - port (str): The database server port.
    - username (str): The username for the database.
    - password (str): The password for the database.
    - db_name (str): The name of the database.

    Returns:
    - engine: A SQLAlchemy engine instance.
    
    Raises:
    - ValueError: If the specified database type is unsupported.
    """
    # Define URLs for different database types
    db_urls = {
        'sqlite': f'sqlite:///{db_name}.db',
        'postgresql': URL.create(drivername='postgresql', username=username, password=password, host=host, port=port, database=db_name),
        'mysql': URL.create(drivername='mysql+pymysql', username=username, password=password, host=host, port=port, database=db_name),
        'mssql': URL.create(drivername='mssql+pyodbc', username=username, password=password, host=host, port=port, database=db_name, query={'driver': 'ODBC Driver 17 for SQL Server'}),
        'oracle': URL.create(drivername='oracle', username=username, password=password, host=host, port=port, database=db_name)
    }
    
    # Check if the specified database type is supported
    if db_type not in db_urls:
        raise ValueError(f"Unsupported database type: {db_type}")

    # Create and return the SQLAlchemy engine
    engine = create_engine(db_urls[db_type], pool_size=10, max_overflow=20)
    return engine

def test_connection(engine):
    """
    Test the database connection.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.

    Returns:
    - bool: True if connection is successful, False otherwise.
    """
    try:
        # Attempt to connect to the database
        connection = engine.connect()
        connection.close()
        logger.info('Database connection successful.')
        return True
    except Exception as e:
        # Log and return False if connection fails
        logger.error(f'Error connecting to database: {e}')
        return False
