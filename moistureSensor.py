class moistureSensor:

    def __init__(self):
        #init GPIO
        #393 = immersed in nute solution, 670 = immersed in just-soaked clay balls, 770 = 9.5 hours after last soaking (i.e. fully wilted), 730 = 2 hrs from last soaking
        self.__max = 820
        self.__min = 393

    def getMoisture(self):
        return 600

    def getMin(self):
        return self.__min

    def getMax(self):
        return self.__max
