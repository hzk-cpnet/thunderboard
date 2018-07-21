from bluepy import btle
from bluepy.btle import *
import struct
from time import sleep


class Thunderboard:

   def __init__(self, dev):
      self.dev  = dev
      self.char = dict()
      self.name = ''
      self.session = ''
      self.coinCell = False
      self.ble_service = None

      # Get device name and characteristics
      scanData = dev.getScanData()

      for (adtype, desc, value) in scanData:
          if (desc == 'Complete Local Name'):
              self.name = value

      self.ble_service = Peripheral()
      self.ble_service.connect(dev.addr, dev.addrType)
      characteristics = self.ble_service.getCharacteristics()

      for k in characteristics:
         if k.uuid == '2a6e':
            self.char['temperature'] = k

         elif k.uuid == '2a6f':
            self.char['humidity'] = k

         elif k.uuid == '2a19':
            self.char['batterylevel'] = k

         elif k.uuid == '2a76':
            self.char['uvIndex'] = k

         elif k.uuid == '2a6d':
            self.char['pressure'] = k

         elif k.uuid == 'c8546913-bfd9-45eb-8dde-9f8754f4a32e':
            self.char['ambientLight'] = k

         elif k.uuid == 'c8546913-bf02-45eb-8dde-9f8754f4a32e':
            self.char['sound'] = k

         elif k.uuid == 'efd658ae-c401-ef33-76e7-91b00019103b':
            self.char['co2'] = k

         elif k.uuid == 'efd658ae-c402-ef33-76e7-91b00019103b':
            self.char['voc'] = k

         elif k.uuid == 'ec61a454-ed01-a5e8-b8f9-de9ec026ec51':
            self.char['power_source_type'] = k


         # elif k.uuid == 'b7c4b694-bee3-45dd-ba9f-f3b5e994f49a':
         #    ch=k.getHandle()
         #    self.ble_service.setDelegate( MyDelegate(ch))  #set notify
         #    ConfigHndl = k.valHandle + 1
         #    self.ble_service.writeCharacteristic(ConfigHndl , (1).to_bytes(2, byteorder='little'))
         #    pass
         #
         # elif k.uuid == 'c4c1f6e2-4be5-11e5-885d-feff819cdc9f':
         #    ch=k.getHandle()
         #    self.ble_service.setDelegate( MyDelegate(ch))  #set notify
         #    ConfigHndl = k.valHandle + 1
         #    self.ble_service.writeCharacteristic(ConfigHndl , (1).to_bytes(2, byteorder='little'))
         #    pass

   def waitForNotification(self):
       if self.ble_service.waitForNotifications(1.0):
           print("Waiting...")

   def enabelNotification(self):
       self.ble_service.setDelegate( MyDelegate())  #set notify
       self.ble_service.writeCharacteristic(79 , (1).to_bytes(2, byteorder='little'))
       self.ble_service.writeCharacteristic(82 , (1).to_bytes(2, byteorder='little'))

   def disabelNotification(self):
      self.ble_service.setDelegate( MyDelegate())  #set notify
      self.ble_service.writeCharacteristic(79 , (0).to_bytes(2, byteorder='little'))
      self.ble_service.writeCharacteristic(82 , (0).to_bytes(2, byteorder='little'))

   def readTemperature(self):
      value = self.char['temperature'].read()
      value = struct.unpack('<H', value)
      value = value[0] / 100
      return value

   def readHumidity(self):
      value = self.char['humidity'].read()
      value = struct.unpack('<H', value)
      value = value[0] / 100
      return value

   def readAmbientLight(self):
      value = self.char['ambientLight'].read()
      value = struct.unpack('<L', value)
      value = value[0] / 100
      return value

   def readUvIndex(self):
      value = self.char['uvIndex'].read()
      value = ord(value)
      return value

   def readCo2(self):
      value = self.char['co2'].read()
      value = struct.unpack('<h', value)
      value = value[0]
      return value

   def readVoc(self):
      value = self.char['voc'].read()
      value = struct.unpack('<h', value)
      value = value[0]
      return value

   def readSound(self):
      value = self.char['sound'].read()
      value = struct.unpack('<h', value)
      value = value[0] / 100
      return value

   def readPressure(self):
      value = self.char['pressure'].read()
      value = struct.unpack('<L', value)
      value = value[0] / 1000
      return value

   def readBatteryLevel(self):
      value = self.char['batterylevel'].read()
      value = struct.unpack('B', value)
      value = value[0]
      return value


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):

        print('')
        if cHandle ==81 :
            print('orientation:')
            result = list(struct.unpack('hhh',data))
            print("x: " + str(result[0]/float(100)))
            print("y: " + str(result[1]/float(100)))
            print("z: " + str(result[2]/float(100)))

        if cHandle ==78 :
            print('acceleration:')
            result = list(struct.unpack('hhh',data))
            print("x: " + str(result[0]/float(1000)) +'g')
            print("y: " + str(result[1]/float(1000)) +'g')
            print("z: " + str(result[2]/float(1000)) +'g')
