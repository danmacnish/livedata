import sys
import time, datetime
import thread
from Traffic import Traffic
import Queue
from DummyPump import Pump #use dummy class for dev on windows
from moistureSensor import moistureSensor

class Plant:
    def __init__(self):
        #turns pump on and off @ relay 1
        self.__pump = Pump(1)
        self.pumpDuration = 5 #num seconds to turn the pump on for

    def calcPumpDuration(self):
        #calculate pump duration based on error between current moisture and traffic data
        self.__duration = 10

def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = False
    data = Queue.Queue()
    try:
        thread.start_new_thread(getData, (data, NO_INTERNET, 5))
        thread.start_new_thread(controlPlant, (data,))
    except:
        print('could not create threads')
    while True:
        time.sleep(1)


#function to get data, log data to file
def getData(queue ,internet, pollPeriod):
    trfc = Traffic()
    trfc.connectToServer(internet)
    while True:
        t = trfc.update(internet)
        #push new delay to queue
        queue.put(t)
        # log average and timestamp to file
        with open('log.txt', 'a') as file:
            file.write(str(t) + ',' + str(datetime.datetime.now()) + '\n')
        file.close()
        time.sleep(pollPeriod*60)

def controlPlant(queue):
    plant = Plant()
    while True:
        print('getting data from queue...')
        try:
            trafficDelay = queue.get()
        except Queue.Empty:
            print('queue empty')


if __name__ == "__main__":
    sys.exit(main())

