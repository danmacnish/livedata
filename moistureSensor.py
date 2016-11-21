import serial
import time, datetime

class moistureSensor:

    def __init__(self):
        #init arduino board
        try:
            self.__serial = serial.Serial('/dev/tty.usbserial', 9600, timeout = 0, write_timeout = 1)
        except serial.SerialException:
            print("can't connect to arduino")
        #393 = immersed in nute solution, 670 = immersed in just-soaked clay balls, 770 = 9.5 hours after last soaking (i.e. fully wilted), 730 = 2 hrs from last soaking
        self.__max = 820
        self.__min = 393

    def getMoisture(self):
        try:
            self.__serial.write(b'1') #write 1 to serial port
        except serial.SerialTimeoutException:
            print('serial port write timeout')
        self.__delay(1000) #wait for arduino to send back data
        try:
            bytes = self.__serial.read(2)
        except serial.SerialException:
            print('couldnt read from serial port')
        moisture = int.from_bytes(bytes, byteorder='big')
        print('soil moisture is ' + str(moisture))
        return moisture

    def getMin(self):
        return self.__min

    def getMax(self):
        return self.__max

    def __delay(self, ms):
        start = datetime.datetime.now()
        delta = datetime.datetime.now() - start
        while(delta.total_seconds()*1000 < ms):
            delta = datetime.datetime.now() - start
