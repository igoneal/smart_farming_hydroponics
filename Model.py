import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import psutil
import time
import datetime
import sqlite3

from matplotlib import pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

timestamp = 1234567890
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# GPIO.cleanup()


# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

sensor1 = adafruit_dht.DHT11(board.D23)

# initialize db connection engine
engine = create_engine('sqlite:///hydrop.db', echo=True)
Session = sessionmaker(bind=engine)

# Define the Base class
Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    name = Column(String)
    pin = Column(Integer)


class Reading(Base):
    __tablename__ = 'reading'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    desc = Column(String)
    value = Column(Float)


# create Table using metadata
Base.metadata.create_all(engine)

# Add sensors to sensors table
session = Session()
#today = str(datetime.date.today())
today = str(time.ctime())
sensor11 = Sensor(date=today, name="DHT 11 Sensor for Temperature & Relative Humidity", pin=23)
session.add_all([sensor11])
session.commit()
session.close()

# Declarative variable for sensor output
while True:
    try:
        temp = sensor1.temperature
        humidity = sensor1.humidity
        # ldr = sensor1.Light_intensity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor1.exit()
        raise error

    # Add readings to reading tables

    session = Session()
    temp_reading = Reading(date=today,desc="Temperature", value=temp)
    hum_reading = Reading(date=today,desc="Relative Humidity", value=humidity)

    sensor11 = Sensor(date=today,name="Temp & RH", pin=23)
    session.add_all([temp_reading, hum_reading])
    session.commit()
    session.close()

    time.sleep(2.0)
