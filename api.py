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
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    #image = get_map.get_map_img(lat,lon)
    response = rooftop_detection.get_roof_type(lat,lon)
    return jsonify(response)
    # if image != 0:
    #     prediction = rooftop_detection.get_prediction(img, ml_project_id, ml_model_id)
    #     roofCategory = prediction.payload[0].display_name
    #     confidence = prediction.payload[0].image_object_detection.score
    #     print(roofCategory)
    #     print(confidence)
    #     #return JSON
    #     return jsonify(
    #     category=roofCategory,
    #     confidence=confidence,
    # )

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