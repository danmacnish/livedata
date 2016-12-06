### livedata
code for Live Data project
Pulls traffic data from the [VicRoads open data platform](http://api.vicroads.vic.gov.au/) and uses the data
to control watering cycles for the plant.

Control system is proportional, with feedback from a soil moisture sensor.

### Control System

  (average traffic delay)---->(*K)----->(+/-)------->(*K2)---------->(Pump)
                                          |
                                          |
  (soil moisture sensor)------------------>
