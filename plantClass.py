import sys
import time, datetime
import thread
from Traffic import Traffic
import Queue

class Plant:
    def __init__(self):
        self.pumpDuration = 5 #num seconds to turn the pump on for

    def calcPumpDuration(self):
        #calculate pump duration based on error between current moisture and traffic data
        self.__duration = 10

def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = False
    data = Queue()
    try:
        thread.start_new_thread(getData, (data, NO_INTERNET, 5))
        thread.start_new_thread(controlPlant, ())
    except:
        print('could not create threads')


#function to get data, log data to file
def getData(q ,internet, pollPeriod):
    trfc = Traffic()
    trfc.connectToServer(internet)
    while True:
        t = trfc.update(internet)
        #push new delay to queue
        q.put(t)
        # log average and timestamp to file
        with open('log.txt', 'a') as file:
            file.write(str(t) + ',' + str(datetime.datetime.now()) + '\n')
        file.close()
        time.sleep(pollPeriod*60)

def controlPlant(q):
    plant = Plant()
    while True:
        print('pump on')
        time.sleep(1)
        print('pump off')
        time.sleep(1)

if __name__ == "__main__":
    sys.exit(main())

