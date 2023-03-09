from peewee import *
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = 'flights'
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = int(os.getenv('DB_PORT'))


db = MySQLDatabase(DB_NAME, host=DB_HOST, port = DB_PORT, user=DB_USER, password=DB_PASSWORD)
class Flight(Model):
   airline_name = CharField(max_length=200)
   airport_depart = CharField(max_length=200)
   airport_arrival = CharField(max_length=200)
   airport_code_depart = CharField(max_length=5)
   airport_code_arrival = CharField(max_length=5)
   datetime_depart = DateTimeField()
   datetime_arrival = DateTimeField()
   flight_duration = TimeField()
   ticket_price = DecimalField(decimal_places=2)
   number_seats_total = IntegerField(null=True)
   number_seats_available = IntegerField()
   number_of_stops = IntegerField()
   connection_flight = BooleanField()
   flight_key = CharField(max_length=300, primary_key=True)
   flight_number = CharField(max_length=20)

   class Meta:
      database=db
      db_table='flights'

def connect_db():
    conn = pymysql.connect(host=DB_HOST, port = DB_PORT, user=DB_USER, password=DB_PASSWORD)
    conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
    conn.close()

    db.connect()
    db.create_tables([Flight])  

def close_db():
   db.close()