import sys
import time, datetime
import thread
from Traffic import Traffic
import Queue
from Pump import Pump #use dummy class for dev on windows
from moistureSensor import moistureSensor

class Plant:
    def __init__(self):
        #turns pump on and off @ relay 1
        self.__pump = Pump(1)
        self.__soil = moistureSensor()
        self.__K = 10 #proportional term for moisture SP calculation
        self.__K2 = 10 #proportional term for pump duration
        self.__Healthy = 430 #moisture level when plant is healthy. moisture measurement ranges from 420 (saturated) to 810 (totally dry)
        self.__pumpBaseDuration = 3000 #pump duration in ms. PID operates around this value.

    def __calcPumpDuration(self, traffic):
        #calculate how wilted we want the plant to be based on the current traffic data, using PID to control soil moisture
        #first calculate the moisture setpoint based on the current traffic (more congestion -> drier soil)
        moistureSP = self.__trafficToMoistureSP(traffic)
        #calculate error term
        error = moistureSP - self.__soil.getMoisture()
        # turn error into pump duration
        pumpDuration = self.__pumpBaseDuration + error * self.__K2
        pumpDuration = self.__clamp(pumpDuration, 0 , 6000) #limit pump duration between 0 and 6 seconds
        self.__pump.setDuration(pumpDuration)
        print(str(datetime.datetime.now()) + ' moisture error is: ' + str(error))

    def __trafficToMoistureSP(self, traffic):
        # calculate the moisture setpoint based on the current traffic (more congestion -> drier soil)
        moistureSP = self.__Healthy + self.__K * traffic
        # Limit value within min/max of moisture SP
        moistureSP = self.__clamp(moistureSP, self.__soil.getMin(), self.__soil.getMax())
        return moistureSP

    def waterPlant(self, traffic):
        self.__calcPumpDuration(traffic)
        self.__pump.water()

    #clamp function to limit values
    def __clamp(self,val, min, max):
        if val > max:
            ret = max
        elif val < min:
            ret = min
        else:
            ret = val
        return ret


def main():
    #set no internet to true to load data from file instead of acquiring from server
    NO_INTERNET = False
    data = Queue.Queue()
    try:
        thread.start_new_thread(getData, (data, NO_INTERNET, 15)) #arguments: queue, flag, period to get new data in minutes
        thread.start_new_thread(controlPlant, (data, 15)) #arguments: queue, watering period
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
        # print average delay
        print("average delay is", t)
        #push new delay to queue
        queue.put(t)
        # log average and timestamp to file
        with open('log.txt', 'a') as file:
            file.write(str(t) + ',' + str(datetime.datetime.now()) + '\n')
        file.close()
        time.sleep(pollPeriod*60)

def controlPlant(queue, period):
    plant = Plant()
    trafficDelay = 0 #initialised to no delay
    while True:
        print('getting data from queue...')
        try:
            trafficDelay = queue.get_nowait()
        except Queue.Empty:
            print('queue empty')
        plant.waterPlant(trafficDelay)
        time.sleep(period*60)

if __name__ == "__main__":
    sys.exit(main())

