class moistureSensor:

    def __init__(self):
        #init GPIO
        self.__max = 820
        self.__min = 420

    def getMoisture(self):
        return 600

    def getMin(self):
        return self.__min

    def getMax(self):
        return self.__max
