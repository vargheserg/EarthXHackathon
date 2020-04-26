import sys, os, json
from . import get_map
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_creds.json"

with open('keys.json', 'r') as f:
    keys = json.load(f)

ml_project_id = keys["ml-project-id"]
ml_model_id = keys["ml-model-id"]

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

def make_recursive_prediction(zoom, latitude, longitude):
  img = get_map.get_map_img(zoom, latitude, longitude)
  if (zoom > 0):
    try:
      prediction = get_prediction(img, ml_project_id, ml_model_id)
      name = prediction.payload[0].display_name
      score = prediction.payload[0].image_object_detection.score
      print (name, score, zoom)
      return name, score, zoom
    except (IndexError, KeyError, TypeError):
      zoom -= 1
      newName, newScore, newZoom = make_recursive_prediction(zoom, latitude, longitude)
      return newName, newScore, newZoom
  else: return 0


def get_roof_type(latitude, longitude):
  zoom = 21
  name, score, finalZoom = make_recursive_prediction(zoom, latitude, longitude)
  response = {}
  response["name"]=name
  response["score"]=score
  return response

lat = 43.521740
longi = -79.847493

get_roof_type(lat, longi)