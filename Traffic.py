from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import json

class Traffic:
    kwargs = {
        'AUTH': 'eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'}
    APItoken = 'AUTH=eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'

    def __init__(self):
        #open connection to get JSON traffic data
        self.__wfs = WebFeatureService(url='http://api.vicroads.vic.gov.au/vicroads/wfs?' + APItoken,
                                version='1.1.0',
                                username=None,
                                password=None, )

        #open connection to get map tiles with traffic lines
        self.__wms = WebMapService('http://api.vicroads.vic.gov.au/vicroads/wms?' + APItoken,
                            version='1.1.1', username=None,
                            password=None,
                            )

    #get traffic data inside bounding box in JSON format
    #bounding box coords
    def __getJSON(self, boundingBox=(144.967260, -37.810767, 144.998717, -37.790761)):
        print "getting JSON traffic data"
        self.__JSONdata = self.__wfs.getfeature(typename='vicroads:bluetooth_links',
                                  bbox = boundingBox,
                                  outputFormat='application/json',
                                  **kwargs
                                  )

    def __processJSON(self):
        #process JSON data
        print "processing JSON traffic data"
        out = open('data.json', 'w')
        out.write(self.__getJSON.read())
        out.close()

    def updateTraffic(self):
        __traffic = 100
        self.__getJSON()
        self.__processJSON()
        return __traffic




wfs = WebFeatureService(url='http://api.vicroads.vic.gov.au/vicroads/wfs?' + APItoken,
                        version='1.1.0',
                        username=None,
                        password=None, )
list(wfs.contents)
response = wfs.getfeature(typename='vicroads:bluetooth_links',
                          bbox=(144.967260, -37.810767, 144.998717, -37.790761),
                          outputFormat='application/json',
                          **kwargs
                          )
out = open('data.json', 'w')
out.write(response.read())
out.close()



img = wms.getmap(layers=['bluetooth_links'],
                 styles=['purple_line'],
                 srs='EPSG:4326',
                 bbox=(144.967260, -37.810767, 144.998717, -37.790761),
                 size=(780, 330),
                 format='image/png',
                 **kwargs
                 )
out = open('tile.png', 'wb')
out.write(img.read())
out.close()
