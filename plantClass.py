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
        self.__soil = moistureSensor()
        self.__K = 50
        self.__Heathly = 600 #moisture level when plant is healthy. moisture measurement ranges from 420 (saturated) to 810 (totally dry)

    def calcPumpDuration(self, traffic):
        #calculate how wilted we want the plant to be based on the current traffic data, using PID to control soil moisture
        #first calculate the moisture setpoint based on the current traffic (more congestion -> drier soil)
        moistureSP = self.__Healthy + self.__K * traffic
        #Limit value within min/max of moisture SP
        moistureSP = self.__clamp(moistureSP, self.__soil.getMin(), self.__soil.getMax())
        #calculate error term
        error = moistureSP - self.__soil.getMoisture()
        print('moisture error is: ',error)

    #clamp function to limit values
    def __clamp(self,val, min, max):
        return max(min(max, val), min)


def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = False
    data = Queue.Queue()
    try:
        thread.start_new_thread(getData, (data, NO_INTERNET, 10))
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
        #traffic.update returns the average delay in minutes for the area. 0 = normal free flowing traffic, -ve is faster than usual, +ve is slower traffic
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
    trafficDelay = 0 #initialised to no delay
    while True:
        print('getting data from queue...')
        try:
            trafficDelay = queue.get()
        except Queue.Empty:
            print('queue empty')
        plant.calcPumpDuration(trafficDelay)

if __name__ == "__main__":
    sys.exit(main())

