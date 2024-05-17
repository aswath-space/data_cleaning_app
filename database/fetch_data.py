import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data(engine, table_name, chunksize=None):
    """
    Fetch data from the specified table in the database.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.
    - table_name (str): The name of the table to fetch data from.
    - chunksize (int, optional): Number of rows to fetch at a time. If None, fetch all data at once.

    Returns:
    - pd.DataFrame: DataFrame containing the fetched data, or None if an error occurs.
    """
    try:
        # Execute the SQL query to fetch data
        with engine.connect() as connection:
            query = f'SELECT * FROM {table_name}'
            if chunksize:
                # Fetch data in chunks if chunksize is specified
                chunks = pd.read_sql(query, connection, chunksize=chunksize)
                df = pd.concat(chunks, ignore_index=True)
            else:
                # Fetch all data at once
                df = pd.read_sql(query, connection)
        logger.info(f'Successfully fetched data from {table_name}.')
        return df
    except Exception as e:
        # Log and return None if fetching data fails
        logger.error(f'Error fetching data from {table_name}: {e}')
        return None

def insert_data(engine, table_name, df):
    """
    Insert data into the specified table in the database.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.
    - table_name (str): The name of the table to insert data into.
    - df (pd.DataFrame): DataFrame containing the data to insert.

    Returns:
    - None
    """
    try:
        # Insert the DataFrame into the specified table
        with engine.connect() as connection:
            df.to_sql(table_name, connection, if_exists='append', index=False)
        logger.info(f'Successfully inserted data into {table_name}.')
    except Exception as e:
        # Log if inserting data fails
        logger.error(f'Error inserting data into {table_name}: {e}')

def update_data(engine, table_name, set_clause, where_clause):
    """
    Update data in the specified table in the database.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.
    - table_name (str): The name of the table to update.
    - set_clause (str): The SET clause of the update statement.
    - where_clause (str): The WHERE clause of the update statement.

    Returns:
    - None
    """
    try:
        # Execute the SQL query to update data
        with engine.connect() as connection:
            query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
            connection.execute(query)
        logger.info(f'Successfully updated data in {table_name}.')
    except Exception as e:
        # Log if updating data fails
        logger.error(f'Error updating data in {table_name}: {e}')

def delete_data(engine, table_name, where_clause):
    """
    Delete data from the specified table in the database.
    
    Parameters:
    - engine: A SQLAlchemy engine instance.
    - table_name (str): The name of the table to delete data from.
    - where_clause (str): The WHERE clause of the delete statement.

    Returns:
    - None
    """
    try:
        # Execute the SQL query to delete data
        with engine.connect() as connection:
            query = f'DELETE FROM {table_name} WHERE {where_clause}'
            connection.execute(query)
        logger.info(f'Successfully deleted data from {table_name}.')
    except Exception as e:
        # Log if deleting data fails
        logger.error(f'Error deleting data from {table_name}: {e}')
