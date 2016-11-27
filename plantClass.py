import sys
import time, datetime
import thread
from Traffic import Traffic
import Queue
from Pump import Pump #use dummy class for dev on windows
from moistureSensor import moistureSensor

class Plant:
    def __init__(self):
        self.__pump = Pump(1) #turns pump on and off @ relay 1
        self.__soil = moistureSensor()
        self.__K = 10 #proportional term for moisture SP calculation
        self.__K2 = 250 #proportional term for pump duration
        self.__Healthy = 450 #moisture level when plant is healthy. moisture measurement ranges from 420 (saturated) to 810 (totally dry)
        self.__pumpBaseDuration = 10000 #pump duration in ms. PID operates around this value.
        self.__pumpDuration = 10000
        self.__error = 0

    def __calcPumpDuration(self, traffic):
        #calculate how wilted we want the plant to be based on the current traffic data, using PID to control soil moisture
        #first calculate the moisture setpoint based on the current traffic (more congestion -> drier soil)
        moistureSP = self.__trafficToMoistureSP(traffic)
        #calculate error term
        self.__error = moistureSP - self.__soil.getMoisture()
        # turn error into pump duration
        self.__pumpDuration = self.__pumpBaseDuration - self.__error * self.__K2
        self.__pumpDuration = self.__clamp(self.__pumpDuration, 0 , 15000) #limit pump duration between 0 and 6 seconds
        self.__pump.setDuration(self.__pumpDuration)

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

    def log(self):
        try:
            with open('logPlantData.txt', 'a') as file:
                file.write(str(datetime.datetime.now()) + ', '
                           + str(self.__soil.getMoisture()) + ', '
                           + str(self.__error) + ', '
                           + str(self.__pumpDuration) + '\n')
            file.close()
        except IOError:
            print(str(datetime.datetime.now()) + " couldn't log plant data to file")


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
        print("average traffic delay in carlton is " + str(t) + ' minutes')
        #push new delay to queue
        queue.put(t)
        # log average delay to file
        trfc.log()
        # print data for a random street every two seconds until we are ready to get fresh traffic data
        for x in range(0, pollPeriod*20):
            trfc.printRandomData()
            time.sleep(3)


def controlPlant(queue, period):
    plant = Plant()
    trafficDelay = 0 #initialised to no delay
    while True:
        try:
            trafficDelay = queue.get_nowait()
        except Queue.Empty:
            #if no data in queue then just operate on previous data
            print('watering the plant')
        plant.waterPlant(trafficDelay)
        #log moisture data and pump duration once per minute until next watering cycle
        for x in range(0, period):
            plant.log()
            time.sleep(60)

if __name__ == "__main__":
    sys.exit(main())

