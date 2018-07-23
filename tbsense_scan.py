from bluepy.btle import *
from bluepy import btle
import struct
from time import sleep
from tbsense import Thunderboard, MyDelegate
import threading

def getThunderboards():
    scanner = Scanner(0)
    devices = scanner.scan(3)
    tbsense = dict()
    for dev in devices:
        scanData = dev.getScanData()
        for (adtype, desc, value) in scanData:
            if desc == 'Complete Local Name':
                if 'Thunder Sense #' in value:
                    deviceId = int(value.split('#')[-1])
                    tbsense[deviceId] = Thunderboard(dev)
    return tbsense

def sensorLoop(tb, devId):

    value = tb.char['power_source_type'].read()
    if ord(value) == 0x04:
        tb.coinCell = True

    while True:
        text = ''
        text += '\n' + tb.name + '\n'
        text += 'CoinCell:\t' + str(tb.coinCell) +'\n'
        data = dict()

        try:

            for key in tb.char.keys():
                if key == 'batterylevel':
                    data['batterylevel'] = tb.readBatteryLevel()
                    text += 'BatteryLevel:\t{} %\n'.format(data['batterylevel'])

                elif key == 'temperature':
                    data['temperature'] = tb.readTemperature()
                    text += 'Temperature:\t{} C\n'.format(data['temperature'])

                elif key == 'humidity':
                    data['humidity'] = tb.readHumidity()
                    text += 'Humidity:\t{} %RH\n'.format(data['humidity'])

                elif key == 'ambientLight':
                    data['ambientLight'] = tb.readAmbientLight()
                    text += 'Ambient Light:\t{} Lux\n'.format(data['ambientLight'])

                elif key == 'uvIndex':
                    data['uvIndex'] = tb.readUvIndex()
                    text += 'UV Index:\t{}\n'.format(data['uvIndex'])

                elif key == 'co2' and tb.coinCell == False:
                    data['co2'] = tb.readCo2()
                    text += 'eCO2:\t\t{}\n'.format(data['co2'])

                elif key == 'voc' and tb.coinCell == False:
                    data['voc'] = tb.readVoc()
                    text += 'tVOC:\t\t{}\n'.format(data['voc'])

                elif key == 'sound':
                    data['sound'] = tb.readSound()
                    text += 'Sound Level:\t{}\n'.format(data['sound'])

                elif key == 'pressure':
                    data['pressure'] = tb.readPressure()
                    text += 'Pressure:\t{}\n'.format(data['pressure'])

        except:
            return
        tb.enabelNotification()
        print(text)
        sleep(1)



if __name__ == '__main__':

    #fb = Thundercloud()
    try:
        thunderboards = getThunderboards()
    except:
        pass

    while True:
        if len(thunderboards) == 0:
            print("No Thunderboard Sense devices found!")
            try:
                thunderboards = getThunderboards()
            except:
                pass
        else:
            try:
                for devid,tb in thunderboards.items():
                    sensorLoop(tb,devid)
            except:
                thunderboards = dict()
                print("reconncting...")
#                pass
                # handleNotification() was called
