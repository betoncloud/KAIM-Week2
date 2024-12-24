import numpy as np
import os
from decimal import  Decimal
from dotenv import load_dotenv
import psycopg2


# Load environment variables from .env file
load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



def clean_missing_data(data, option,column):

    try:
        if option =='remove' and column!='':
            data=data.dropna(subset=[column], how='any')

        elif option=='replace_with_default':
            data.fillna({'column': 0}, inplace=True)

        elif option == 'replace_with_mean':
            mean_value = data[column].mean()
            data[column].fillna(mean_value, inplace=True)

        elif option =='replace_with_mode':
            mode_value = data[column].mode()[0]  
            data[column].fillna(mode_value, inplace=True)
        else:
            data
        print('successfully completed')
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def clean_outlier(data, option,column):

    try:      
        column_mean=data[column].mean()
        std_dev = data[column].std()
        upper_bound = column_mean + 3 * std_dev
        lower_bound = column_mean - 3 * std_dev

        if option =='replace_with_mean' and column!='':            
            data[column] = data[column].apply(lambda x: column_mean if x < lower_bound or x > upper_bound else x)

        elif option=='replace_with_min':
            min_value = data[column].min()
            data[column] = data[column].apply(lambda x: min_value if x < lower_bound or x > upper_bound else x)
        else:
            data
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def update_database(data_clean):
    try:
        conn = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        for index, row in data_clean.iterrows():
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE xdr_data
                SET session_frequency = ?, duration = ?, data_volume = ?
                WHERE id = ?
                ''', (row['session_frequency'], row['duration'], row['data_volume'], row['id']))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def insert_scores(data):
    # Load environment variables from .env file
    load_dotenv()


    connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
    )
   
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO user_scores (user_id, engagement_score, experience_score, satisfaction_score)
        VALUES (%s, %s, %s, %s)
        """

    data = data.astype({
            "MSISDN/Number": "string",
            "Engagement_Score": "string",
            "Experience_Score": "string",
            "Satisfaction_Score": "string"
    })

    for index, row in data.iterrows():
        cursor.execute(insert_query, ( row['MSISDN/Number'], row['Engagement_Score'],  row['Experience_Score'],  row['Satisfaction_Score']    ))

    connection.commit()
    cursor.close()
    connection.close()
