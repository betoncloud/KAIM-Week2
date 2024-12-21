import numpy as np
import os

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
        Q1 = column.quantile(0.25)
        Q3 = column.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        if option =='replace_with_mean' and column!='':
            column_mean=column.mean()
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


def calculate_dispersion(column):
    try:
        # 1. Range
        data_range = column.max() - column.min()

        # 2. Variance
        data_variance = column.var()

        # 3. Standard Deviation
        data_std_dev = column.std()

        # 4. Interquartile Range (IQR)
        Q1 = column.quantile(0.25)
        Q3 = column.quantile(0.75)
        data_iqr = Q3 - Q1

        # 5. Coefficient of Variation (CV)
        mean = column.mean()
        data_cv = data_std_dev / mean
        # Return results as a dictionary
        return {
            "Data Range": data_range,
            "Data Variance": data_variance,
            "Data STD DEV": data_std_dev,
            "Data IQR": data_iqr,
            "Data CV": data_cv,
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def update_database(data_clean,):
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


