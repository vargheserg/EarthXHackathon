from flask import Flask, request, jsonify
from detector import rooftop_detection as rd
from flask_cors import CORS

import os
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '<h1>Deployed to Wherever! </h1>'
    #Environment variables: os.environ['varName']

@app.route('/process', methods=['GET'])
def stuff():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    sol = float(request.args.get('solar'))
    response = rd.get_roof_data(lat,lon)
    image = response['image']
    #response.pop('image', None)
    coeffecient = {
      "prism": 0.75, 
      "flat": 1, 
      "slantedprism": 0.6, 
      "pyramid": 0.5, 
      "complex": 0.4
    }
    response["adjusted"]=coeffecient[response["name"]] * sol
    return jsonify(response)
    

if __name__ == "__main__":
  app.run()

# Sample request
# {
#     "methods": "GET",
#     "solar": "3.121",
#     "lat": "7.721321321313",
#     "lon": "7.721321321313",
# }


# Sample response
# {
#     "category": "slantedprism",
#     "image": image,
#      "calculatedArea":"something something m^2",
#      "powerRating":"something something kWh/ m^2",
# }