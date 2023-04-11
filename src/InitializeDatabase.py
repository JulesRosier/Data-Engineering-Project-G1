import os
import mysql.connector

database = "DWVluchten"
host = "localhost"
user = "root"
password = os.environ.get('MYSQL_PASSWORD')

#AirportKey = 1
AirportCodes = ['CRL', 'BRU', 'ANR', 'LGG', 'OST', 'CFU', 'BDS', 'NAP', 'ALC', 'RHO', 'AGP', 'PMI', 'HER', 'PMO','FAO', 'TFS', 'IBZ']
Landen = ["Belgium", "Greece", "Spain", "Italy", "Portugal"]
TimeZones = {}




mydb = mysql.connector.connect(
  host= host,
  user= user,
  password=password,
  database=database
)
mycursor = mydb.cursor()



#drop = write mysql query with variable database to drop database

def MakeNewDatabase():

  drop = "DROP DATABASE IF EXISTS {};".format(database)
  mycursor.execute(drop)

  create = "CREATE DATABASE IF NOT EXISTS {};".format(database)
  mycursor.execute(create)




def MakeDimAirport():

  makeDimAirportTable = ("CREATE TABLE DWVluchten.DimAirport"
                        "(AirportKey INT PRIMARY KEY,"
                        "AirportCode VARCHAR(3),"
                        "AirportName VARCHAR(50),"
                        "City VARCHAR(50),"
                        "Country VARCHAR(50),"
                        "UNIQUE KEY `AirportCode` (`AirportCode`));")
  mycursor.execute(makeDimAirportTable)



  fillDimAirport = ("INSERT INTO DWVluchten.DimAirport "
                    "(AirportKey, AirportCode) "
                    "VALUES (%s, %s)")

  # i vervangen door AirportKey indien nodig  
  for i, AirportCode in enumerate(AirportCodes):
    mycursor.execute(fillDimAirport, (i+1, AirportCode)) 

def FillDimAirport():
  fillDimAirportQuery = ('UPDATE DWVluchten.DimAirport SET '
        'AirportName = CASE'
            ' WHEN AirportCode = "BRU" THEN "Brussels Airport Zaventem"'
            ' WHEN AirportCode = "CRL" THEN "Brussels South Charleroi Airport"'
            ' WHEN AirportCode = "ANR" THEN "Antwerp Airport"'
            ' WHEN AirportCode = "OST" THEN "Ostend-Bruges International Airport"'
            ' WHEN AirportCode = "LGG" THEN "Liege Airport"'
            ' WHEN AirportCode = "CFU" THEN "Corfu Airport"'
            ' WHEN AirportCode = "HER" THEN "Heraklion Airport"'
            ' WHEN AirportCode = "RHO" THEN "Rhodes Airport"'
            ' WHEN AirportCode = "ALC" THEN "Alicante Airport"'
            ' WHEN AirportCode = "IBZ" THEN "Ibiza Airport"'
            ' WHEN AirportCode = "AGP" THEN "Malaga Airport"'
            ' WHEN AirportCode = "PMI" THEN "Palma de Mallorca Aiport"'
            ' WHEN AirportCode = "TFS" THEN "Tenerife South Airport"'
            ' WHEN AirportCode = "BDS" THEN "Brindisi Airport"'
            ' WHEN AirportCode = "NAP" THEN "Napels International Airport"'
            ' WHEN AirportCode = "PMO" THEN "Palermo Airport"'
            ' WHEN AirportCode = "FAO" THEN "Faro Airport"'
            'ELSE NULL '
            'END, '
        'City = CASE '
            ' WHEN AirportCode = "BRU" THEN "Brussels"'
            ' WHEN AirportCode = "CRL" THEN "Charleroi"'
            ' WHEN AirportCode = "ANR" THEN "Antwerp"'
            ' WHEN AirportCode = "OST" THEN "Ostend"'
            ' WHEN AirportCode = "LGG" THEN "Liege"'
            ' WHEN AirportCode = "CFU" THEN "Corfu"'
            ' WHEN AirportCode = "HER" THEN "Heraklion"'
            ' WHEN AirportCode = "RHO" THEN "Rhodes island"'
            ' WHEN AirportCode = "ALC" THEN "Alicante"'
            ' WHEN AirportCode = "IBZ" THEN "Balearen"'
            ' WHEN AirportCode = "AGP" THEN "Málaga"'
            ' WHEN AirportCode = "PMI" THEN "Palma, Balearic Islands"'
            ' WHEN AirportCode = "TFS" THEN "Santa Cruz de Tenerife"'
            ' WHEN AirportCode = "BDS" THEN "Brindisi"'
            ' WHEN AirportCode = "NAP" THEN "Napels"'
            ' WHEN AirportCode = "PMO" THEN "Metropolitan City of Palermo"'
            ' WHEN AirportCode = "FAO" THEN "Faro"'
            'ELSE NULL '
            'END, '
        'Country =  CASE '
            ' WHEN 	AirportCode = "BRU" OR '
                    'AirportCode = "CRL" OR '
                    'AirportCode = "ANR" OR '
                    'AirportCode = "OST" OR '
                    'AirportCode = "LGG" '
            ' THEN "Belgium"'
            ' WHEN 	AirportCode = "CFU" OR '
                    'AirportCode = "HER" OR '
                    'AirportCode = "RHO" '
            ' THEN "Greece"'
            ' WHEN 	AirportCode = "ALC" OR '
                    'AirportCode = "IBZ" OR '
                    'AirportCode = "AGP" OR '
                    'AirportCode = "PMI" OR '
                    'AirportCode = "TFS" '
                ' THEN "Spain"'
            ' WHEN 	AirportCode = "BDS" OR '
                    'AirportCode = "NAP" OR '
                    'AirportCode = "PMO" '
            ' THEN "Italy"'
            ' WHEN 	AirportCode = "FAO" '
            ' THEN "Portugal"'
            'ELSE NULL '
            'END'
            ';')
  
  mycursor.execute(fillDimAirportQuery)

def MakeDimAirline():
  makeDimAirlineTable = (
    'CREATE TABLE DWVluchten.DimAirline ('
    'AirlineKey INT PRIMARY KEY,'
    'AirlineCode VARCHAR(2),'
    'AirlineName VARCHAR(50),'
    'AirlineContact VARCHAR(50),'
    'AirlineAddress VARCHAR(100),'
    'UNIQUE KEY `AirlineCode` (`AirlineCode`)'
    ');'
    )
  mycursor.execute(makeDimAirlineTable)

def MakeAirlineKeys():
  #nog te genereren
  codes = GetAirlineCodes()
  keys = []
  for i in range(len(codes)):
    keys.append(i+1)
  return keys

def GetAirlineCodes():
  return ['SN', 'TB', 'FR']
  # return df.airline_iata_code.unique()

def addAirlineKeys():
  table = 'DimAirline'
  AirlineKeys = MakeAirlineKeys()
  AirlineCodes = GetAirlineCodes()
  CodeDict = dict(zip(AirlineKeys, AirlineCodes)) #codes samen voegen in dict
  AddAirlineKeysQuery = ('INSERT INTO {}.{} (AirlineKey, AirlineCode) '
                         'VALUES (%s, %s)'.format(database, table))
  values = [(key, value) for key, value in CodeDict.items()]
  mycursor.executemany(AddAirlineKeysQuery, values)

def FillDimAirline():
  fillDimAirlineTable = (
    'UPDATE DWVluchten.DimAirline SET '
    'AirlineName = CASE '
				' WHEN AirlineCode = "SN" THEN "Brussels Airlines"'
        ' WHEN AirlineCode = "TB" THEN "TUIfly"'
        ' WHEN AirlineCode = "FR" THEN "Ryanair"'
        'ELSE NULL '
        'END, '
    'AirlineContact = CASE '
				' WHEN AirlineCode = "SN" THEN "+32 2 723 23 62"'
        ' WHEN AirlineCode = "TB" THEN "+32 2 717 86 61"'
        ' WHEN AirlineCode = "FR" THEN "+32 7 848 21 30"'
        'ELSE NULL '
        'END, '
    'AirlineAddress = CASE '
				' WHEN AirlineCode = "SN" THEN "Jaargetijdenlaan 100-102, 1050 Elsene, België"'
        ' WHEN AirlineCode = "TB" THEN "Luchthaven Brussel Nationaal, 40 Bus 1, 1930 Zaventem,  België"'
        ' WHEN AirlineCode = "FR" THEN "Airside Business Park, Swords, Co. Dublin,Ireland"'
        'ELSE NULL '
        'END;'
  )
  mycursor.execute(fillDimAirlineTable)

def RemoveNumbers():
  dropSmall = 'DROP TABLE IF EXISTS DWVluchten.numbers_small;'
  dropNumbers = 'DROP TABLE IF EXISTS DWVluchten.numbers;'

  mycursor.execute(dropSmall)
  mycursor.execute(dropNumbers)

def MakeNumbers():

  RemoveNumbers()

  createSmall = 'CREATE TABLE DWVluchten.numbers_small (number INT);'
  mycursor.execute(createSmall)

  insertSmall = 'INSERT INTO DWVluchten.numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);'
  mycursor.execute(insertSmall)

  
  createNumbers = 'CREATE TABLE DWVluchten.numbers (number BIGINT);'
  mycursor.execute(createNumbers)
  insertNumbers = ('INSERT INTO DWVluchten.numbers '
  'SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number '
  'FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones '
  'LIMIT 1000000;')
  mycursor.execute(insertNumbers)


def MaakDimDate():
  maakDimDate = ('CREATE TABLE DWVluchten.DimDate ('
  'DateKey BIGINT PRIMARY KEY, '
  'FullDateAlternateKey DATETIME, '
  'EnglishDayNameOfWeek VARCHAR(10), '
  'DutchDayNameOfWeek VARCHAR(50), '
  'DayOfWeek TINYINT, '
  'DayOfMonth TINYINT, '
  'DayOfYear SMALLINT, '
  'WeekOfMonth TINYINT, '
  'WeekOfYear TINYINT, '
  'MonthOfYear TINYINT, '
  'EnglishMonthName VARCHAR(10), '
  'DutchMonthName VARCHAR(10), '
  'Quarter TINYINT, '
  'Year SMALLINT, '
  'Holiday BOOLEAN, '
  'NameHoliday VARCHAR(50), '
  'BelgianVacation varchar(50), '
  #'-- Weekend VARCHAR(10), '
  'Weekend BOOLEAN,  '
  'UNIQUE KEY `FullDateAlternateKey` (`FullDateAlternateKey`) '
  ');')
  mycursor.execute(maakDimDate)

def FillDimDateKeys():
  pass

def FillDimDate():
  pass

def MakeDimFlight():
  pass

def FillDimFlight():
  #komt later, unieke waarden uit csv
  pass

def MakeFactFlight():
  pass

def FillFactFlight():
  #komt later, alle data in factflight
  pass



def InitializeDatabase():
  MakeNewDatabase()

  MakeDimAirport()
  FillDimAirport()

  MakeDimAirline()
  addAirlineKeys()
  FillDimAirline()
  
  MakeNumbers()
  
  MaakDimDate()
  FillDimDateKeys()
  FillDimDate()

  MakeDimFlight()

  MakeFactFlight()

  RemoveNumbers() #verwijderen van tijdelijke tabellen

InitializeDatabase()

#Uploaden naar db
mydb.commit()


print("Geslaagd")