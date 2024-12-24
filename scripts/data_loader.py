

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load environment variables from .env file
load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_data_from_postgres(query):
    """
    Connects to the PostgreSQL database and loads data based on the provided SQL query.

    :param query: SQL query to execute.
    :return: DataFrame containing the results of the query.
    """
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        # Load data using pandas
        df = pd.read_sql_query(query, connection)

        # Close the database connection
        connection.close()

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def load_data_using_sqlalchemy(query):
    """
    Connects to the PostgreSQL database and loads data based on the provided SQL query using SQLAlchemy.

    :param query: SQL query to execute.
    :return: DataFrame containing the results of the query.
    """
    try:
        # Create a connection string
        connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        # Create an SQLAlchemy engine
        engine = create_engine(connection_string)

        # Load data into a pandas DataFrame
        df = pd.read_sql_query(query, engine)

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def execute_query(query):
    try:
         # Create a connection string
        connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        # Create an SQLAlchemy engine
        engine = create_engine(connection_string)

        # Load data into a pandas DataFrame
        result = pd.read_sql_query(query, engine)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def top_5_handsets_for_top_3_manufacturers():
    try:
        query = """
        WITH TopManufacturers AS (
    
        SELECT 
         "Handset Manufacturer", 
        count(distinct "IMEI") AS total_devices
        FROM xdr_data
        where "Handset Manufacturer" is not null
        GROUP BY "Handset Manufacturer"
        ORDER BY total_devices DESC
        LIMIT 3
        ),

        RankedHandsets AS (
   
        SELECT 
        h."Handset Manufacturer",
        h."Handset Type",
        tm.total_devices,
        ROW_NUMBER() OVER (PARTITION BY h."Handset Manufacturer" ORDER BY tm.total_devices DESC) AS rank
        FROM xdr_data h
        
        INNER JOIN TopManufacturers tm ON h."Handset Manufacturer" = tm."Handset Manufacturer"
		where "Handset Type" is not null
        )
        SELECT 
        "Handset Manufacturer",
	    "Handset Type"
    
        FROM RankedHandsets
        WHERE rank <= 5
        ORDER BY "Handset Manufacturer", rank;
        """
        
        df = execute_query(query)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None