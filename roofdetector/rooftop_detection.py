#opencv-python-4.2.0.34
import sys, os, json, math, cv2
import get_map
import numpy as np
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
      
      box = prediction.payload[0].image_object_detection.bounding_box.normalized_vertices
      x1 = box[0].x*800
      y1 = box[0].y*800
      x2 = box[1].x*800
      y2 = box[1].y*800
      return img, name, score, x1, y1, x2, y2, zoom
    except (IndexError, KeyError, TypeError):
      zoom -= 1
      return make_recursive_prediction(zoom, latitude, longitude)
  else: return 0

def get_roof_size(rType,x1,y1,x2,y2, latitude, zoom):
  metersPerPx = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
  widthM = (x2-x1)*metersPerPx
  lengthM = (y2-y1)*metersPerPx
  angle = 30
  area = 0

  if rType == "flat":
    area = widthM*lengthM
  elif rType == "pyramid":
    height = widthM/2 * math.tan(math.radians(angle))
    area = ((widthM*height)/2)*4
  elif rType == "prism":
    area = ((lengthM*widthM)/(2*math.cos(math.radians(angle))))*4
  elif rType == "slantedprism":
    wid = min(widthM, lengthM)
    len = max(widthM, lengthM)
    triangles = ((wid/(2*math.sin(math.radians(angle))))*wid)*2
    rects = ((wid/(2*math.cos(math.radians(angle))))*len)*2
    area = triangles + rects
  elif rType == "complex": 
    #same calc as slantedprism cuz most complex ones have this general shape
    wid = min(widthM, lengthM)
    len = max(widthM, lengthM)
    triangles = ((wid/(2*math.sin(math.radians(angle))))*wid)*2
    rects = ((wid/(2*math.cos(math.radians(angle))))*len)*2
    area = triangles + rects
  
  return area

def draw_box(img, x1, y1, x2, y2):
  print(x1,x2,y1,y2)
  start = (int(x1),int(y1))
  end = (int(x2),int(y2))
  print (start, end)
  image = np.asarray(bytearray(img), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  cv2.rectangle(image, start, end, 0, 2)
  cv2.imwrite("my.png",image)

  cv2.imshow("lalala", image)
  k = cv2.waitKey(0)


def get_roof_data(latitude, longitude):
  zoom = 20
  image, name, score, x1, y1, x2, y2, endZoom = make_recursive_prediction(zoom, latitude, longitude)
  get_roof_size(name, x1,y1,x2,y2, latitude, endZoom)
  draw_box(image, x1, y1, x2, y2)
  #print(name, score, box, finalZoom)

if __name__ == "__main__":
  lat = 43.521740
  longi = -79.847493

  get_roof_data(lat, longi)
