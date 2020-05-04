import cv2, base64
import numpy as np

from detector import get_size as gs
from detector import get_prediction as gp

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
  return png_as_text

def get_roof_data(latitude, longitude):
  zoom = 20
  image, name, score, x1, y1, x2, y2, endZoom = gp.make_recursive_prediction(zoom, latitude, longitude)
  size = gs.get_roof_size(name, x1,y1,x2,y2, latitude, endZoom)

  image = draw_box(image, x1, y1, x2, y2)

  response = {}
  response['image']=str(image)[2:-1]
  response['name']=name
  response['score']=score
  response['size']=size
  return response

if __name__ == "__main__":
  lat = 43.7322193485497874
  longi = -79.6181400203285

  get_roof_data(lat, longi)
