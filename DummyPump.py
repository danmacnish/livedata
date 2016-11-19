import pifacerelayplus
import time, datetime

class Pump:
    def __init__(self, num):
        # init GPIO
        self.__relayNumber = num
        self.__relays = pifacerelayplus.PiFaceRelayPlus(None,7) #piface board is configured with address 7, and no expansion board
        self.period = 1  # time to turn light on
        self.duration = 2  # time to turn light off

    def on(self):
        #turn pump on
        self.__relays[self.__relayNumber].turn_on()
        print(str(datetime.datetime.now()) + ' pump on')

    def off(self):
        self.__relays[self.__relayNumber].turn_off()
        print(str(datetime.datetime.now()) + ' pump off')

