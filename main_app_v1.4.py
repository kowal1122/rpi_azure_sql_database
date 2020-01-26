#!/usr/bin/python
import pyodbc
import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT) #33
GPIO.setup(19, GPIO.OUT) #35
GPIO.setup(15, GPIO.OUT) #37
signal = 0

# read data using pin 14
instance = dht11.DHT11(pin=14)

conn = pyodbc.connect('DRIVER={freetds};SERVER=inteligentny-dom.database.windows.net;PORT=1433;DATABASE=inteligentny-dom;UID=admin2020;PWD=fg63*id1;TDS_VERSION=8.0')


def read(conn):
    print("Read")
    cursor = conn.cursor()
    #Sample select query
    cursor.execute("SELECT * FROM [dbo].[measurements]") 
    row = cursor.fetchone() 
    while row: 
        print(str(row[1]) + " " + str(row[0])+ " " + str(row[2])+ " " + str(row[3])+ " " + str(row[4]))
        row = cursor.fetchone()
    
    

def update(conn):
    print("Update")
    
try:
        while True:
            result = instance.read()
            if result.is_valid():
                now = datetime.datetime.now()
                godzina = now.strftime("%H:%M:%S")
                data = datetime.date.today()
                
                print("Data pomiaru: " + str(data))
                print("godzina pomiaru: " + str(godzina))
                print("Temperatura: %-3.1f C" % result.temperature)
                print("wilgotnosc: %-3.1f %%" % result.humidity)
                print("----------------" + str(signal))
                GPIO.output(19, GPIO.HIGH)
                
                if result.temperature > 24:
                    print("powyzej 24!!!")
                    GPIO.output(15, GPIO.HIGH)
                    signal = 1
                    
                else:
                    print("poniżej 24!")
                    GPIO.output(15, GPIO.LOW)
                    signal = 0
                    
                cursor = conn.cursor()
                  
                cursor.execute("INSERT INTO measurements VALUES ('" + str(data) + "', '" + str(godzina) + "', '" + str(result.temperature) + "', '" + str(signal) + "');")
                conn.commit()
                
                time.sleep(8)
                GPIO.output(26, GPIO.HIGH)
                time.sleep(2)     
                GPIO.output(26, GPIO.LOW)

             

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
    
finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 
#read(conn)

#MAIN 
update(conn)

conn.close()
