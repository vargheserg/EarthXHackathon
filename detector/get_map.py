import requests, urllib, json

with open('keys.json', 'r') as f:
    keys = json.load(f)

maps_static_key = keys["maps-static"]

imagewidth = 400
imageheight = 400
scale = 2

def get_map(zoom, latitude, longitude):
   url = "https://maps.googleapis.com/maps/api/staticmap?"
   center = str(latitude) + "," + str(longitude)

   urlparams = urllib.parse.urlencode({'center': center,
                                          'zoom': str(zoom),
                                          'size': str(imagewidth) + 'x' + str(imageheight),
                                          'maptype': 'satellite',
                                          'sensor': 'false',
                                          'scale': str(scale), 
                                          'key': maps_static_key})
   print(url + urlparams)
   r = requests.get(url + urlparams)

   if not (r.status_code==404 or r.status_code==403):
      return r.content
   else:
      return 0

