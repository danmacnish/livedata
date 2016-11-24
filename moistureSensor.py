from pyfirmata import Arduino, util
import time, datetime


class moistureSensor:

    def __init__(self):
        #init arduino board
        self.__board = None
        try:
            self.__board = Arduino('/dev/ttyACM0')
            self.__it = util.Iterator(self.__board)
            self.__it.start()
            self.__board.analog[0].enable_reporting()
            time.sleep(3) #wait for firmata to initialise
        except:
            print("can't connect to arduino")
        #393 = immersed in nute solution, 670 = immersed in just-soaked clay balls, 770 = 9.5 hours after last soaking (i.e. fully wilted), 730 = 2 hrs from last soaking
        self.__max = 820
        self.__min = 393

    def getMoisture(self):
        moisture = -1
        if self.__board is not None:
            try:
                moisture = self.__board.analog[0].read() * 1024
            except:
                print('failed to read analog 0 from arduino')
            print(str(datetime.datetime.now()) + ' soil moisture is ' + str(moisture))
        else:
            print('firmata not initialised, cant get moisture')
        return moisture

    def getMin(self):
        return self.__min

    def getMax(self):
        return self.__max
