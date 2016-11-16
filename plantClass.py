import sys
import time, datetime
from Traffic import Traffic

class Plant:
    def __init__(self):
        self.pumpDuration = 5 #num seconds to turn the pump on for

    def calcPumpDuration(self):
        #calculate pump duration based on error between current moisture and traffic data
        self.__duration = 10

def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = False
    trfc = Traffic()
    while True:
        t = trfc.update(NO_INTERNET)
        #log average and timestamp to file
        with open('log.txt', 'a') as file:
            file.write(str(t) + ',' + str(datetime.datetime.now()) + '\n')
        file.close()
        time.sleep(880) #wait for 880 seconds

if __name__ == "__main__":
    sys.exit(main())
