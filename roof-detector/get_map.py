import requests, urllib, json

with open('keys.json', 'r') as f:
    keys = json.load(f)

maps_static_key = keys["maps-static"]

def get_map_img(latitude, longitude):
   url = "https://maps.googleapis.com/maps/api/staticmap?"
   center = str(latitude) + "," + str(longitude)

   urlparams = urllib.parse.urlencode({'center': center,
                                          'zoom': '21',
                                          'size': '400x400',
                                          'maptype': 'satellite',
                                          'sensor': 'false',
                                          'scale': '2', 
                                          'key': maps_static_key})
   print(url + urlparams)
   r = requests.get(url + urlparams)

   if not (r.status_code==404 or r.status_code==403):
      return r.content
   else:
      return 0

