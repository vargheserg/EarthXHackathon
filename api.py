from flask import Flask, request, jsonify
from roofdetector import get_map as get_map
from roofdetector import rooftop_detection as rooftop_detection
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
    response = rooftop_detection.get_roof_data(lat,lon)
    image = response['image']
    response.pop('image', None)
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