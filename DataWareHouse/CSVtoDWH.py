import os
import mysql.connector

DATABASE = "DWVluchten"
HOST = "localhost"
USER = "root"
PASSWORD = os.environ.get('DB_PASSWORD')

def Connect():
    try:
        conn = mysql.connector.connect(
            host=HOST, 
            database=DATABASE, 
            user=USER, 
            password=PASSWORD)
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except:
        print("Error while connecting to MySQL")

conn = Connect()
cursor = conn.cursor()

def FillFactFlight():
    pass

def FillDimFlight():
    pass