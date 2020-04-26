#opencv-python-4.2.0.34
import sys, os, json, math, cv2, base64
from roofdetector import get_map
import numpy as np
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
import requests
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

  if (zoom > 18):
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
  print("zoom",zoom)
  if zoom == 21: 
    metersPerPx = 2/44
  elif zoom == 20: 
    metersPerPx = 5/55
  elif zoom == 19: 
    metersPerPx = 10/55
  else: 
    metersPerPx = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom))/234
  
  #metersPerPx = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom))

  widthM = (x2-x1)*metersPerPx
  lengthM = (y2-y1)*metersPerPx
  print (widthM, lengthM, 400*metersPerPx)
  angle = 30
  area = 0
  area = widthM*lengthM  
  return area

def draw_box(img, x1, y1, x2, y2):
  start = (int(x1),int(y1))
  end = (int(x2),int(y2))
  image = np.asarray(bytearray(img), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)

  cv2.rectangle(image, start, end, 0, 4)
  #cv2.imshow("lalala", image)
  #k = cv2.waitKey(0)
  
  b64img= cv2.imencode('.png', image)[1].tostring()
  retval, buffer = cv2.imencode('.png', image)
  png_as_text = base64.b64encode(buffer)
  #response = requests.post(test_url, data=base64.b64encode(b64img), headers=headers)
  #print(png_as_text)
  return png_as_text

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
  response['image']=str(image)[2:-1]
  response['name']=name
  response['score']=score
  response['size']=size
  return response

if __name__ == "__main__":
  lat = 43.73212274448905
  longi = -79.61853123719736

  get_roof_data(lat, longi)
