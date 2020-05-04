import time
import sys

# Lys, avstand (proximity)
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from datetime import datetime

# CSV
import csv
from csv import writer

# BME280 sensor for temperatur/trykk/fuktigheit
bme280 = BME280()

# PMS5003 partikkelsensor
pms5003 = PMS5003()

# Hovudloopen
try:
    while True:
        with open('data.csv', mode='w', newline='') as datafil: # mode='a' legg til nye data, 'w' skriv over
            dataskriver = writer(datafil)

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
        
        # Legg saman data i ei liste
        listeAlleData = [tidspunkt,dataTemp,dataTrykk,dataFukt,dataLys,dataPM1,dataPM25,dataPM10]

        # Skriv innhaldet i lista til CSV-fila
        dataskriver.writerow(listeAlleData)
        print("Data er skrive til CSV-fil.")
        
        # Sover 5 sek mellom kvar registrering
        print("Ventar litt...")
        time.sleep(5)
        
# Kontrollert avslutning
except KeyboardInterrupt:
    print("Avsluttar...")
    sys.exit(0)