import sys, os, json
import get_map
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

  name = 'projects/***REMOVED******REMOVED***/locations/us-central1/models/***REMOVED******REMOVED***'.format(project_id, model_id)
  payload = ***REMOVED***'image': ***REMOVED***'image_bytes': content ***REMOVED******REMOVED***
  params = ***REMOVED******REMOVED***
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned


def get_roof_type(latitude, longitude):
  img = get_map.get_map_img(latitude, longitude)
  if (img != 0):
    prediction = get_prediction(img, ml_project_id, ml_model_id)
    print (prediction.payload[0].display_name)
    print (prediction.payload[0].image_object_detection.score)
    return prediction.payload[0].display_name

lat = 43.521740
longi = -79.847493

get_roof_type(lat, longi)