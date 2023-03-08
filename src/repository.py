from peewee import *
import pymysql

DB_NAME = 'flights'


db = MySQLDatabase(DB_NAME, host='localhost', port = 3306, user='root', password='toor')
class Flight(Model):
   airline_name = CharField(max_length=200)
#    airport_depart = CharField(max_length=100)
#    airport_arrival = CharField(max_length=100)
   airport_code_depart = CharField(max_length=5)
   airport_code_arrival = CharField(max_length=5)
   datetime_depart = DateTimeField()
   datetime_arrival = DateTimeField()
   flight_duration = TimeField()
   ticket_price = DecimalField(decimal_places=2)
   number_seats_total = IntegerField()
   number_seats_available = IntegerField()
   number_of_stops = IntegerField()
   connection_flight = BooleanField()
   flight_key = CharField(max_length=300, primary_key=True)
   flight_number = CharField(max_length=20)


   class Meta:
      database=db
      db_table='flights'


def connect_db():
    conn = pymysql.connect(host='localhost', user='root', password='toor')
    conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
    conn.close()

    db.connect()
    db.create_tables([Flight])  

def close_db():
   db.close()