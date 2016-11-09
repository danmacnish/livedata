import sys
from Traffic import Traffic

class Plant:
    def __init__(self):
        self.pumpDuration = 5 #num seconds to turn the pump on for

    def calcPumpDuration(self):
        #calculate pump duration based on error between current moisture and traffic data
        self.__duration = 10

def main():
    trfc = Traffic()
    t = trfc.update()
    print(t)

if __name__ == "__main__":
    sys.exit(main())
