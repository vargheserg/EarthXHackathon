import overpass

api = overpass.API()
response = api.Get('node["name"="Salt Lake City"]')
print(str(response))