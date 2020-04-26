#opencv-python-4.2.0.34
import sys, os, json, math, cv2, base64
from roofdetector import get_map
import numpy as np
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_creds.json"

with open('keys.json', 'r') as f:
    keys = json.load(f)

ml_project_id = keys["ml-project-id"]
ml_model_id = keys["ml-model-id"]

imagewidth = 400
imageheight = 400
scale = 2

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
  img = get_map.get_map_img(zoom, latitude, longitude)

  if (zoom > 0):
    # Try running the following code without errors
    try:
      # make a prediction on the image
      prediction = get_prediction(img, ml_project_id, ml_model_id)

      center = ((imagewidth*scale)/2,(imageheight*scale)/2)
      dists = []

      # iterate through each detection and calculate their distance to the center
      for i in range (0, len(prediction.payload)):
        detection = prediction.payload[i]
        box = detection.image_object_detection.bounding_box.normalized_vertices
        x1 = box[0].x*imageheight*scale
        y1 = box[0].y*imageheight*scale
        x2 = box[1].x*imageheight*scale
        y2 = box[1].y*imageheight*scale
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
      x1 = box[0].x*imageheight*scale
      y1 = box[0].y*imageheight*scale
      x2 = box[1].x*imageheight*scale
      y2 = box[1].y*imageheight*scale
      return img, name, score, x1, y1, x2, y2, zoom
    
    # if no detections are found, zoom out and recursively run the function over again
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
  start = (int(x1),int(y1))
  end = (int(x2),int(y2))
  image = np.asarray(bytearray(img), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  cv2.rectangle(image, start, end, 0, 4)
  b64img = base64.b64encode(image)
  return b64img

def get_roof_data(latitude, longitude):
  zoom = 20
  image, name, score, x1, y1, x2, y2, endZoom = make_recursive_prediction(zoom, latitude, longitude)
  size = get_roof_size(name, x1,y1,x2,y2, latitude, endZoom)

  output = "\n\nDetected roof at ({},{})\n\
Type: {}\n\
Confidence: {} %\n\
Surface Area: {} Meters".format(str(latitude), str(longitude),name, int(score*100), str(int(size)))
  print(output)
  image = draw_box(image, x1, y1, x2, y2)


  response = {}
  response['image']=image
  response['name']=name
  response['score']=score
  response['size']=size
  return response

if __name__ == "__main__":
  lat = 43.521740
  longi = -79.847493

  get_roof_data(lat, longi)
