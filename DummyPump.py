import time, datetime

class Pump:
    def __init__(self, num):
        # init GPIO
        self.__relayNumber = num
        self.period = 1  # time to turn light on
        self.duration = 2  # time to turn light off

    def on(self):
        #turn pump on
        print(str(datetime.datetime.now()) + ' pump on')

    def off(self):
        print(str(datetime.datetime.now()) + ' pump off')

