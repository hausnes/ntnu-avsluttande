import time
import colorsys
import os
import sys
#import ST7735
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from subprocess import PIPE, Popen
import logging
from datetime import datetime
import csv

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
pms5003 = PMS5003()

# Create a values dict to store the data
variables = ["temperature",
             "pressure",
             "humidity",
             "light",
             "oxidised",
             "reduced",
             "nh3",
             "pm1",
             "pm25",
             "pm10"]

listeAlleVerdata = []

# The main loop
try:
    while True:
        with open('data.csv', mode='w', newline='') as datafil: # mode='a' legg til nye data, 'w' skriv over
            
            dataskriver = csv.writer(datafil)
            
            # Informasjon om tidspunkt for avlesing
            tidspunkt = datetime.now()
            print("Tidspunkt akkurat no:",tidspunkt)

            # Temperatur, C
            enhet = "C"
            dataTemp = bme280.get_temperature()
            print(dataTemp,enhet)

            # Trykk, hPa
            enhet = "hPa"
            dataTrykk = bme280.get_pressure()
            print(dataTrykk,enhet)

            # Fuktighet
            enhet = "%"
            dataFukt = bme280.get_humidity()
            print(dataFukt,enhet)

            # Lyssensor
            enhet = "Lux"
            dataLys = ltr559.get_lux()
            print(dataLys,enhet)

            # Partiklar, pm1
            enhet = "ug/m3 (pm1)"
            try:
                dataPM1 = pms5003.read()
            except pmsReadTimeoutError:
                print("Feil ved avlesing av PMS5003")
            else:
                dataPM1 = float(dataPM1.pm_ug_per_m3(1.0))
                print(dataPM1,enhet)

            # Partiklar, pm2.5
            enhet = "ug/m3 (pm2.5)"
            try:
                dataPM25 = pms5003.read()
            except pmsReadTimeoutError:
                print("Feil ved avlesing av PMS5003")
            else:
                dataPM25 = float(dataPM25.pm_ug_per_m3(2.5))
                print(dataPM25,enhet)

            # Partiklar, pm10
            enhet = "ug/m3 (pm10)"
            try:
                dataPM10 = pms5003.read()
            except pmsReadTimeoutError:
                print("Feil ved avlesing av PMS5003")
            else:
                dataPM10 = float(dataPM10.pm_ug_per_m3(10))
                print(dataPM10,enhet)
        
        
        # Sjoelve skrivinga
        dataskriver.writerows(listeAlleVerdata)
        print("Data er skrive til CSV-fil.")
        
        # Sover 5 sek mellom kvar registrering
        print("Ventar litt...")
        time.sleep(5)
        
# Kontrollert avslutning
except KeyboardInterrupt:
    print("Avsluttar...")
    sys.exit(0)

'''
# Tomme lister ved oppstart
listeTemperaturar = []
listeLuftfuktighet = []
listeCO2 = []
listeAlleVerdata = []

def returnerAlleVerdata():
    print("---")

# Ein funksjon som registrer over tid, heilt til brukaren avsluttar med CTRL+C
def registrerSaaLenge():
    kjorer = True
    while kjorer:
        try:
            listeAlleVerdata.append(returnerAlleVerdata())
            print("Legg til data i lista med alle verdata.")
            time.sleep(0.5)
        except KeyboardInterrupt:
            kjorer = False
            print("Avsluttar registrering.")
            print(listeAlleVerdata)

registrerSaaLenge()

'''
#Skrive verdata til CSV-fil, basert paa listene fraa funksjonen registrerSaaLenge()
'''
print("-------------------------")
with open('data.csv', mode='w', newline='') as datafil: # mode='a' legg til nye data, 'w' skriv over
    dataskriver = csv.writer(datafil)
    dataskriver.writerows(listeAlleVerdata)
    print("Data er skrive til CSV-fil.")
    #dataskriver.writerows([verdi] for verdi in listeTemperaturar) # Brukte denne naar eg berre hadde tall (temperatur), ikkje tidskode. Skjoenar ikkje kvifor det var noedvendig.

'''