import math

def get_roof_size(rType,x1,y1,x2,y2, latitude, zoom):
  if zoom == 21: 
    metersPerPx = 2/46
  elif zoom == 20: 
    metersPerPx = 5/57
  elif zoom == 19: 
    metersPerPx = 10/57
  else: 
    metersPerPx = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom))/234
  
  widthM = (x2-x1)*metersPerPx
  lengthM = (y2-y1)*metersPerPx
  area = widthM*lengthM 
  print(area, widthM, lengthM)

  return area

    
