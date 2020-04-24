import codecs
import osm2geojson

with codecs.open('file.osm', 'r', encoding='utf-8') as data:
    xml = data.read()

geojson = osm2geojson.xml2geojson(xml)
# >> ***REMOVED*** "type": "FeatureCollection", "features": [ ... ] ***REMOVED***

