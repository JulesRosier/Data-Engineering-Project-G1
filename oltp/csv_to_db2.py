import mysql.connector as mysql
from mysql.connector import Error
from datetime import date, timedelta
import shutil
import os
from dotenv import load_dotenv

# Moet 2 keer runnen als DB nog niet bestaat, idk why

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = "flight_oltp"
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

CSV_FOLDER = "./src/csv/"

BASE_OUT_DIR = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\"
DATA_OUT = BASE_OUT_DIR + 'All.csv'
FLIGHT_OUT = BASE_OUT_DIR + 'LoadInfo.csv'


LOAD_FILES_SQL = "./oltp/LoadFiles.sql"
LOAD_INFO_SQL = "./oltp/LoadInfo.sql"

conn = mysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
c = conn.cursor()
c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_DATABASE}")
c.close()
conn.close()

try:
    # autocommit is zéér belangrijk.
    conn = mysql.connect(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True,
    )
    print(type(conn))
    if conn.is_connected():
        if os.path.exists(DATA_OUT):
            print(f"Deleted {DATA_OUT}")
            os.remove(DATA_OUT)

        if os.path.exists(FLIGHT_OUT):
            print(f"Deleted {FLIGHT_OUT}")
            os.remove(FLIGHT_OUT)

        for file in os.listdir(CSV_FOLDER):
            conn.reconnect()
            if file.endswith('.csv'):
                if file.startswith('All_'):
                    print(f'Loading {file}... ', end='')
                    shutil.copy(os.path.join(CSV_FOLDER, file), DATA_OUT)

                    cursor = conn.cursor(dictionary=True)
                    with open(LOAD_FILES_SQL, 'r') as sql_file:
                        result_iterator = cursor.execute(sql_file.read(), multi=True)

                    cursor.close()
                    print('DONE')

                if file.startswith('info_flight'):
                    print(f'Loadinf {file}... ', end='')
                    shutil.copy(os.path.join(CSV_FOLDER, file), FLIGHT_OUT)

                    cursor = conn.cursor(dictionary=True)
                    try:
                        cursor.execute("CREATE INDEX idx_flight_nr ON flight_fixed_data(flight_number)")
                    except:
                        pass
                    with open(LOAD_INFO_SQL, 'r') as sql_file:
                        result_iterator = cursor.execute(sql_file.read(), multi=True)
                    cursor.close()
                    print('DONE')


        print("Seeding... ", end='')
        conn.reconnect()
        cursor = conn.cursor()
        with open("./oltp/Seeds.sql", "r") as f:
            cursor.execute(f.read(), multi=True)
        cursor.close()
        print("DONE")

    conn.close()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")