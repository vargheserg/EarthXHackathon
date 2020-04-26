import os, json, math
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

from detector import get_map as gm

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

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

def make_recursive_prediction(zoom, latitude, longitude):
  # Gets image of map from lat and long
  img = gm.get_map(zoom, latitude, longitude)

  if (zoom > 18):
    # Try running the following code without errors
    try:
      # make a prediction on the image
      prediction = get_prediction(img, ml_project_id, ml_model_id)

      center = ((gm.imagewidth*gm.scale)/2,(gm.imageheight*gm.scale)/2)
      dists = []

      # iterate through each detection and calculate their distance to the center
      for i in range (0, len(prediction.payload)):
        detection = prediction.payload[i]
        box = detection.image_object_detection.bounding_box.normalized_vertices
        x1 = box[0].x*gm.imageheight*gm.scale
        y1 = box[0].y*gm.imageheight*gm.scale
        x2 = box[1].x*gm.imageheight*gm.scale
        y2 = box[1].y*gm.imageheight*gm.scale
        boxcenter = ((x1+x2)/2,(y1+y2)/2)
        distToCenter = calculateDistance(boxcenter[0], boxcenter[1], center[0],center[1])
        dists.append((distToCenter,i))

      # find the box closest to the center of the frame
      closestDist = dists[0]
      for box in dists:
        if box[0] < closestDist[0]:
          closestDist = box

      # return values of the closest box
      payload = prediction.payload[closestDist[1]]
      name = payload.display_name
      score = payload.image_object_detection.score
      box = payload.image_object_detection.bounding_box.normalized_vertices
      x1 = box[0].x*gm.imageheight*gm.scale
      y1 = box[0].y*gm.imageheight*gm.scale
      x2 = box[1].x*gm.imageheight*gm.scale
      y2 = box[1].y*gm.imageheight*gm.scale
      return img, name, score, x1, y1, x2, y2, zoom
    
    # if no detections are found, zoom out and recursively run the function over again
    except (IndexError, KeyError, TypeError):
      zoom -= 1
      return make_recursive_prediction(zoom, latitude, longitude)
  else: return 0