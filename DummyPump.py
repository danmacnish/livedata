import time, datetime

class Pump:
    def __init__(self, num):
        # init GPIO
        self.__relayNumber = num
        self.period = 1  # time to turn light on
        self.__duration = 2  # time to turn light off

    def __on(self):
        #turn pump on
        print(str(datetime.datetime.now()) + ' pump on')

    def __off(self):
        print(str(datetime.datetime.now()) + ' pump off')

    def setDuration(self, duration):
        self.__duration = duration

    def water(self):
        print(str(datetime.datetime.now()) + ' watering plant for ' + str(self.__duration) + ' ms')
        self.__on()
        self.__delay(self.__duration)
        self.__off()

    def __delay(self, ms):
        start = datetime.datetime.now()
        delta = datetime.datetime.now() - start
        while(delta.total_seconds()*1000 < ms):
            delta = datetime.datetime.now() - start

