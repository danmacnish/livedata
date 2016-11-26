import pifacerelayplus
import time, datetime

class Pump:
    def __init__(self, num):
        # init GPIO
        self.__relayNumber = num
        self.__relays = pifacerelayplus.PiFaceRelayPlus(None,chip_select = 1) #piface board is configured with address 7, and no expansion board
        self.period = 1  # time to turn light on
        self.__duration = 2  # time to turn light off

    def __on(self):
        #turn pump on
        self.__relays.relays[self.__relayNumber].turn_on()

    def __off(self):
        self.__relays.relays[self.__relayNumber].turn_off()

    def setDuration(self, duration):
        self.__duration = duration

    def water(self):
        print(str('watering plant for ' + str(self.__duration/1000) + ' seconds')
        self.__on()
        self.__delay(self.__duration)
        self.__off()

    def __delay(self, ms):
        start = datetime.datetime.now()
        delta = datetime.datetime.now() - start
        while (delta.total_seconds() * 1000 < ms):
            delta = datetime.datetime.now() - start