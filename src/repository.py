import datetime
import json
from peewee import *
import pymysql
from dotenv import load_dotenv
import requests
import os
import time

load_dotenv()

DB_NAME = 'flights'
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = int(os.getenv('DB_PORT'))

print(DB_HOST, DB_USER, DB_PASSWORD, DB_PORT)
time.sleep(3)
conn = pymysql.connect(host=DB_HOST, port = DB_PORT, user=DB_USER, password=DB_PASSWORD)
conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
conn.close()
db = MySQLDatabase(DB_NAME, host=DB_HOST, port = DB_PORT, user=DB_USER, password=DB_PASSWORD)

class BaseModel(Model):
   class Meta:
      Database = db

class Airline(BaseModel):
   id = IntegerField(primary_key=True)
   name = CharField(max_length=100)

   class Meta:
      database=db
      db_table='airlines'


class Airport(BaseModel):
   code = CharField(max_length=5, primary_key=True)
   full_name = CharField(max_length=200, null=True)

   class Meta:
      database=db
      db_table='airports'

class Flight(BaseModel):
   last_updated = DateTimeField(default=datetime.datetime.now)

   airline_id = ForeignKeyField(Airline, null=True)

   airport_code_depart = ForeignKeyField(Airport)
   airport_code_arrival = ForeignKeyField(Airport)

   datetime_depart = DateTimeField()
   datetime_arrival = DateTimeField()
   flight_duration = TimeField()
   ticket_price = DecimalField(decimal_places=2)
   number_seats_total = IntegerField(null=True)
   number_seats_available = IntegerField()
   number_of_stops = IntegerField(null=True)
   connection_flight = BooleanField(null=True)
   flight_key = CharField(max_length=300, primary_key=True)
   flight_number = CharField(max_length=20)

   class Meta:
      database=db
      db_table='flights'

def connect_db():
    db.create_tables([Airline, Airport, Flight])  



ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
DEPART = ['BRU', 'ANR', 'OST', 'LGG', 'CRL']
URL = "https://kuvsche4de.execute-api.eu-central-1.amazonaws.com/prod/airportname?airportCode={code}&language=nl"
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def seed_db():
   Airline.get_or_create(id = 1, name ='Ryanair')
   Airline.get_or_create(id = 2, name ='BrusselsAirline')
   Airline.get_or_create(id = 3, name ='TuiFly')
   Airline.get_or_create(id = 4, name ='Transavia')

   for a in (ARIVE + DEPART):
      if not Airport.select().where(Airport.code == a).exists():
         response = requests.get(URL.format(code=a), headers=HEADER)

         full_name = None
         if response.status_code == 200:
            full_name = response.content[1:-1]
         Airport.create(code = a,
                        full_name = full_name)

def close_db():
   db.close()