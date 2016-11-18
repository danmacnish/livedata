from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import time, datetime
import json


class Traffic:
    def __init__(self):
        self.__kwargs = {
            'AUTH': 'eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'}
        self.__APItoken = 'AUTH=eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'
        #how old the traffic data is before it is deemed irrelevant, in seconds
        self.dataExpiry = 1800 #30 minutes

    # get traffic data inside bounding box in JSON format
    # bounding box coords are in EPSG format https://epsg.io/map#srs=4326&x=144.977088&y=-37.791982&z=15
    def __getJSON(self, noInternet=False, boundingBox=(144.967260, -37.810767, 144.998717, -37.790761)):
        if noInternet is False:
            print("getting JSON traffic data from server")
            try:
                #get data from web service
                data = self.__wfs.getfeature(typename='vicroads:bluetooth_links',
                                             bbox=boundingBox,
                                             outputFormat='application/json',
                                             **self.__kwargs
                                             )
                # decode JSON data into python object
                self.__JSONdata = json.load(data)
            except ValueError as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
        else:
            print("loading traffic data from file")
            try:
                with open("JSON/data.json") as json_file:
                    self.__JSONdata = json.load(json_file)
            except IOError as inst:
                print(type(inst))
                print(inst.args)
                print(inst)

    def __processJSON(self):
        # process JSON data
        print("processing JSON traffic data")
        # access and print the data we want (particular rd, etc)
        print(self.__JSONdata['bbox'])
        #build list containing delays with corresponding timestamp
        delays = [(x['properties']['timestamp'],x['properties']['delay']) for x in self.__JSONdata['features']]
        #calculate timedelta and add to delays list
        self.__delays = [dict()]
        for tstamp, delay in delays:
            #YYYY-MM-DDTHH:MM:SS.sss
            (year, month, day, hour, minute, second) = int(tstamp[0:4]), int(tstamp[5:7]), int(tstamp[8:10]), int(tstamp[11:13]), int(tstamp[14:16]), int(tstamp[17:19])
            delta = datetime.datetime.utcnow() - datetime.datetime(year, month, day, hour, minute, second )
            self.__delays.append({'timestamp':tstamp,'delay':delay,'delta':delta})
            #print(delta.total_seconds())
        #remove first element in list because it's empty
        self.__delays.pop(0)
        #calculate average delay, excluding data that's more than 15 minutes old
        recentDelays = [x['delay'] for x in self.__delays if x['delta'].total_seconds() < self.dataExpiry]
        self.__averageDelay = sum(recentDelays)/len(recentDelays)
        #print average delay
        print("average delay is", self.__averageDelay)
        #print data
        for x in self.__delays:
            print(str(x['timestamp']) + ', ' + str(x['delay']) + ', ' + str(x['delta'].total_seconds()))


    def connectToServer(self, noInternet=False):
        if noInternet is False:
            print('connecting to server')
            # open connection to get JSON traffic data
            self.__wfs = WebFeatureService(url='http://api.vicroads.vic.gov.au/vicroads/wfs?' + self.__APItoken,
                                           version='1.1.0',
                                           username=None,
                                           password=None, )

            # open connection to get map tiles with traffic lines
            self.__wms = WebMapService('http://api.vicroads.vic.gov.au/vicroads/wms?' + self.__APItoken,
                                       version='1.1.1', username=None,
                                       password=None,
                                       )
        else:
            print("no internet connection, will load old data from file instead")

    def update(self, noInternet=False):
        self.__getJSON(noInternet)
        self.__processJSON()
        return self.__averageDelay

# img = wms.getmap(layers=['bluetooth_links'],
#                 styles=['purple_line'],
#                srs='EPSG:4326',
#                 bbox=(144.967260, -37.810767, 144.998717, -37.790761),
#                 size=(780, 330),
#                 format='image/png',
#                 **kwargs
#                 )
# out = open('tile.png', 'wb')
# out.write(img.read())
# out.close()
