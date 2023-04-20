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
DOWNLOADS_FOLDER = "./src/csv/"
OLTP_FOLDER = "./oltp/"
SQL_UPLOAD = "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\"

conn = mysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {DB_DATABASE}")
conn.close()

conn = None
cursor = None

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
        # choose a specific start_date
        start_date = date(2023, 4, 6)
        end_date = date.today()
        delta = timedelta(days=1)
        while start_date <= end_date:

            date_format = start_date.strftime("%Y_%m_%d")

            # for each date check if the file exists and copy the file to C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\
            old_path = DOWNLOADS_FOLDER + "All" + "_" + date_format + ".csv"
            print(old_path)
            new_path = (SQL_UPLOAD + "All" + ".csv")

            # Remove file if it already exists
            if os.path.exists(new_path):
                os.remove(new_path)
            if os.path.exists(old_path):
                shutil.copy(old_path, new_path)

            # conn.reconnect is important, otherwise error
            conn.reconnect()
            cursor = conn.cursor()

            # Execute commands in file LoadFiles.sql to import data into database 'flight_oltp'
            file_name = "LoadFiles.sql"

            with open("{}{}".format(OLTP_FOLDER, file_name), "r") as f:
                cursor.execute(f.read(), multi=True)
            cursor.close()

            start_date += delta

        for file in os.listdir(DOWNLOADS_FOLDER):
            if "info_flightnumber" in file:
                target_path = SQL_UPLOAD + "info.csv"
                if os.path.exists(target_path):
                    os.remove(target_path)
                shutil.copy(DOWNLOADS_FOLDER + file, target_path)
                conn.reconnect()
                cursor = conn.cursor()
                print(f"loading {file}... ", end='')
                with open("./oltp/LoadInfo.sql", "r") as f:
                    cursor.execute(f.read(), multi=True)
                cursor.close()

                # Cleanup
                os.remove(target_path)
                print(f"done")

        print("Seeding... ", end='')
        conn.reconnect()
        cursor = conn.cursor()
        with open("./oltp/Seeds.sql", "r") as f:
            cursor.execute(f.read(), multi=True)
        cursor.close()
        print("done")

    conn.close()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")