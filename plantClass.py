import sys
from Traffic import Traffic

class Plant:
    def __init__(self):
        self.pumpDuration = 5 #num seconds to turn the pump on for

    def calcPumpDuration(self):
        #calculate pump duration based on error between current moisture and traffic data
        self.__duration = 10

def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = True
    trfc = Traffic()
    t = trfc.update(NO_INTERNET)
    print(t)

if __name__ == "__main__":
    sys.exit(main())
