import requests
import json
def getOSM(city):
    url = 'https://nominatim.openstreetmap.org/search?city=' + city + '&format=json'
    # osm_type = response[0]["osm_type"]
    # osm_id = response[0]["osm_id"]
    response = requests.get(url)
    print(response.text)
    print()
    return json.loads(response.text)
    
def getOverpass(osm):
    osm_type = osm[0]["osm_type"]
    osm_id = osm[0]["osm_id"]
    #http://overpass-api.de/api/interpreter?data=[out:json];node(18063533);out;
    url = 'http://overpass-api.de/api/interpreter?data=[out:json];' + osm_type + '(' + str(osm_id) + ');out;'
    response = requests.get(url)
    print(response.text)
    return json.loads(response.text)

# def getGeoJSON(overpass):
#     geojson = {
#         "type": "FeatureCollection",
#         "features": [
#         {
#             "type": "Feature",
#             "geometry" : {
#                 "type": "Point",
#                 "coordinates": [d["lon"], d["lat"]],
#                 },
#             "properties" : d,
#         } for d in overpass]
#     }
#     return geojson

# def convert_json(overpass):
#     return json.dumps({ "type": "FeatureCollection",
#                         "features": [ 
#                                         {"type": "Feature",
#                                          "geometry": { "type": "Point",
#                                                        "coordinates": [ feature['lon'],
#                                                                         feature['lat']]},
#                                          "properties": { key: value 
#                                                          for key, value in feature.items()
#                                                          if key not in ('lat', 'lon') }
#                                          } 
#                                      for feature in overpass
#                                     ]
#                        })



def OSMtoGeoJSON(city):
    geojson = getOverpass(getOSM(city))
    #geojson = convert_json(getOverpass(getOSM(city)))
    print(geojson)

OSMtoGeoJSON('Toronto')