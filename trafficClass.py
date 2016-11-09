from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService

kwargs = {
    'AUTH': 'eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'}
APItoken = 'AUTH=eyJraWQiOiJRRFFQWDZVSDlQRExOOU9GQVowMlNFRFVYIiwic3R0IjoiYWNjZXNzIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiIzd1lpbjFJeHBWWVNiSTZwZkxtQVZMIiwiaWF0IjoxNDc1NTU1NTI2LCJpc3MiOiJodHRwczovL2FwaS5zdG9ybXBhdGguY29tL3YxL2FwcGxpY2F0aW9ucy80QXk3eUYybVFDaUJacVB6OUN5UVU4Iiwic3ViIjoiaHR0cHM6Ly9hcGkuc3Rvcm1wYXRoLmNvbS92MS9hY2NvdW50cy8zdktRd3VTZEQ0OVl3a25Kb1lYTllXIiwiZXhwIjoxNDkxNDUzMTI2fQ.yjUbqzx3df0EtxzOXXX8uHnK-c1X7yiWff1gzGvrv08'

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

wms = WebMapService('http://api.vicroads.vic.gov.au/vicroads/wms?' + APItoken,
                    version='1.1.1', username=None,
                    password=None,
                    )

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
